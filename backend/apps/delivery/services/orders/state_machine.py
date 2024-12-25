from collections.abc import Callable

import attr
from django.utils.timezone import now
from transitions import Machine

from backend.apps.delivery.models import Order


@attr.dataclass
class OrderFSM:
    _order: Order

    # Поля экземпляра после инициализации
    state: Order.State = attr.field(init=False)
    take_the_job: Callable[[], bool] = attr.field(init=False)
    drive_to_customer: Callable[[], bool] = attr.field(init=False)
    customer_paid: Callable[[], bool] = attr.field(init=False)
    cancel: Callable[[], bool] = attr.field(init=False)

    def __attrs_post_init__(self) -> None:
        self._machine = Machine(
            model=self,
            states=Order.State,
            initial=Order.State(self._order.state),
            after_state_change=self._save_state,
        )

        self._machine.add_transition(
            trigger="take_the_job",
            source=Order.State.NEW,
            dest=Order.State.PROCESSING,
        )
        self._machine.add_transition(
            trigger="drive_to_customer",
            source=Order.State.PROCESSING,
            dest=Order.State.DELIVERY,
        )
        self._machine.add_transition(
            trigger="customer_paid",
            source=Order.State.DELIVERY,
            dest=Order.State.PAID,
        )
        self._machine.add_transition(
            trigger="cancel",
            source=[Order.State.NEW, Order.State.PROCESSING, Order.State.DELIVERY],
            dest=Order.State.CANCELED,
        )

    def _save_state(self) -> None:
        self._order.state = self.state
        self._order.state_changed_at = now()
        self._order.save(update_fields=("state", "state_changed_at"))
