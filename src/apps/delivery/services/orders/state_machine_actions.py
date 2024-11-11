from abc import ABC, abstractmethod
from typing import final

from apps.delivery.models import Order
from apps.delivery.services.orders.exceptions import OrderNotFoundError
from apps.delivery.services.orders.state_machine import OrderFSM
from apps.users.models import User


class BaseAction(ABC):
    _user: User
    _order_id: int

    def __init__(self, user: User, order_id: int) -> None:
        self._user = user
        self._order_id = order_id

    def __call__(self) -> None:
        if self._user.is_anonymous or not self._user.role == User.Role.DELIVERY_PARTNER:
            raise OrderNotFoundError

        try:
            order = Order.objects.filter(partner__user=self._user).get(id=self._order_id)
        except Order.DoesNotExist as exc:
            raise OrderNotFoundError from exc

        state_machine = OrderFSM(order)
        self._action(state_machine)

    @abstractmethod
    def _action(self, order_state_machine: OrderFSM) -> None:
        pass


@final
class TakeOrderToJob(BaseAction):
    def _action(self, order_state_machine: OrderFSM) -> None:
        order_state_machine.take_the_job()


@final
class DriveToCustomer(BaseAction):
    def _action(self, order_state_machine: OrderFSM) -> None:
        order_state_machine.drive_to_customer()


@final
class CustomerPaid(BaseAction):
    def _action(self, order_state_machine: OrderFSM) -> None:
        order_state_machine.customer_paid()


@final
class CancelOrder(BaseAction):
    def _action(self, order_state_machine: OrderFSM) -> None:
        order_state_machine.cancel()
