class BaseOrdersReportError(Exception):
    pass


class SenderError(Exception):
    pass


class NotAvailableReportError(BaseOrdersReportError):
    pass
