from enum import StrEnum


class NewOrdersReportType(StrEnum):
    DAILY = "daily"
    EVENING = "evening"


REPORT_TYPE_BY_HOUR = {
    13: NewOrdersReportType.DAILY,
    22: NewOrdersReportType.EVENING,
}
