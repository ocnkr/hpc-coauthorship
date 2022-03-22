from neomodel import (
    StructuredRel,
    IntegerProperty,
)


class AttendedRel(StructuredRel):
    number_of_attendance = IntegerProperty()