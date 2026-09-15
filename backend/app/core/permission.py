from typing import Dict, List, Tuple

PermGroup = Dict[str, List[Tuple[str, str]]]
PERMISSION_DEFINITIONS: Dict[str, PermGroup] = {
    "Dashboard" : {
        "Dashboard" : [
            ("View dashboard", "dashboard.view"),
        ]
    },
    "Employee":{
        "Dashboard": [
            ("View dashboard", "employee.dashboard.view"),
        ],
        "Staff": [
            ("List staff", "employee.staff.list"),
            ("View staff", "employee.staff.view"),
            ("Create staff", "employee.staff.create"),
            ("Update staff", "employee.staff.update"),
            ("Delete staff", "employee.staff.delete"),
        ],
        "Departments": [
            ("List departments", "employee.department.list"),
            ("Create department", "employee.department.create"),
            ("Update department", "employee.department.update"),
            ("Delete department", "employee.department.delete"),
        ],
        "Position": [
            ("List positions", "employee.position.list"),
            ("Create position", "employee.position.create"),
            ("Update position", "employee.position.update"),
            ("Delete position", "employee.position.delete"),
        ],
    },
    "Attendance": {
        "Records": [
            ("View attendance", "attendance.record.view"),
            ("Edit attendance", "attendance.record.update"),
            ("Export attendance", "attendance.record.export"),
        ],
        "Check-in/out": [
            ("Manual check-in", "attendance.checkin.create"),
            ("Manual check-out", "attendance.checkout.create"),
        ],
    },
    'Leave':{
        "Requests": [
            ("List leave requests", "leave.request.list"),
            ("View leave request", "leave.request.view"),
            ("Create leave request", "leave.request.create"),
            ("Approve leave request", "leave.request.approve"),
            ("Reject leave request", "leave.request.reject"),
            ("Cancel leave request", "leave.request.cancel"),
        ],
        "Policy": [
            ("View leave policy", "leave.policy.view"),
            ("Update leave policy", "leave.policy.update"),
        ],
    },
    "Payroll": {
        "Salary": [
            ("View salary", "payroll.salary.view"),
            ("Update salary", "payroll.salary.update"),
        ],
        "Payslips": [
            ("List payslips", "payroll.payslip.list"),
            ("View payslip", "payroll.payslip.view"),
            ("Generate payslip", "payroll.payslip.generate"),
        ],
    },
    "Administration": {
        "Admin Users": [
            ("List admin users", "admin.user.list"),
            ("View admin user", "admin.user.view"),
            ("Create admin user", "admin.user.create"),
            ("Update admin user", "admin.user.update"),
            ("Delete admin user", "admin.user.delete"),
            ("Enable admin user", "admin_users.enable"),     
            ("Disable admin user", "admin_users.disable"),
        ],
        "Roles": [
            ("List roles", "admin.role.list"),
            ("View role", "admin.role.view"),
            ("Create role", "admin.role.create"),
            ("Update role", "admin.role.update"),
            ("Delete role", "admin.role.delete"),
            ("Assign permissions", "admin.role.assign_permissions"),
        ],
    },
    "Settings": {
        "General": [
            ("View settings", "settings.general.view"),
            ("Update settings", "settings.general.update"),
        ],
    },
}