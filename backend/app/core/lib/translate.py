from contextvars import ContextVar
from typing import Optional

# Language codes accepted from clients, mapped to the index used in
# the `translations` lists below: [english, khmer, chinese].
SUPPORTED_LANGUAGES = {
    "en": 0,
    "kh": 1,
    "km": 1,  # ISO 639-1 code for Khmer (Accept-Language sends this)
}
DEFAULT_LANGUAGE = "en"

_language_index = ContextVar("_language_index", default = SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE])

def set_lang(index: int):
    _language_index.set(index)

def get_lang() -> int:
    return _language_index.get()

def resolve_lang(code: Optional[str]) -> int:
    """Map a client language code ('en', 'kh') to a translation
    index, falling back to the default language for unknown/missing codes.
    Accepts raw Accept-Language values like 'km-KH,km;q=0.9'."""
    if not code:
        return SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE]
    primary = code.split(",")[0].split(";")[0].split("-")[0].strip().lower()
    return SUPPORTED_LANGUAGES.get(primary, SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE])

translations = {
    'success': ['Success', 'ជោគជ័យ'],
    'fail': ['Failed', 'បរាជ័យ',],

    'username': ['Username', 'ឈ្មោះអ្នកប្រើ',],
    'password': ['Password', 'ពាក្យសម្ងាត់',],

    'enter_username_pass': [
        'Enter username and password',
        'បញ្ចូលឈ្មោះអ្នកប្រើ និងពាក្យសម្ងាត់',
    ],

    'enter_user': [
        'Enter username',
        'បញ្ចូលឈ្មោះអ្នកប្រើ',
    ],

    'enter_password': [
        'Enter password',
        'បញ្ចូលពាក្យសម្ងាត់',
    ],

    'invalid_username': [
        'Invalid username',
        'ឈ្មោះអ្នកប្រើមិនត្រឹមត្រូវ',
    ],

    'invalid_password': [
        'Invalid password',
        'ពាក្យសម្ងាត់មិនត្រឹមត្រូវ',
    ],

    'invalid_user_password': [
        'Incorrect username or password',
        'ឈ្មោះអ្នកប្រើ ឬពាក្យសម្ងាត់មិនត្រឹមត្រូវ',
    ],

    'server_error': [
        'Server error',
        'កំហុសម៉ាស៊ីនមេ',
    ],

    'invalid_parameters': [
        'Invalid parameters',
        'ប៉ារ៉ាម៉ែត្រមិនត្រឹមត្រូវ',
    ],

    'invalid_token': [
        'Invalid token',
        'Token មិនត្រឹមត្រូវ',
    ],

    'app_token_required': [
        'App token is required!',
        'ត្រូវការសញ្ញា​សម្ងាត់កម្មវិធី!',
    ],

    'invalid_api_key': [
        'Invalid API key',
        'API Key មិនត្រឹមត្រូវ',
    ],

    'invalid_format': [
        'Invalid format',
        'ទម្រង់មិនត្រឹមត្រូវ',
    ],

    'invalid_date_format': [
        'Invalid date format',
        'ទម្រង់កាលបរិច្ឆេទមិនត្រឹមត្រូវ',
    ],

    'data_cannot_empty': [
        'Data is required',
        'ទិន្នន័យត្រូវតែបំពេញ',
    ],

    'field_cannot_empty': [
        'Field cannot empty',
        'ត្រូវតែបំពេញ',
    ],

    'rate_limit_exceeded': [
        'Too many requests',
        'សំណើច្រើនពេក',
    ],

    'request_timed_out': [
        'Request timed out',
        'សំណើអស់ពេល',
    ],

    'record_exist': [
        'Record already exists',
        'មានទិន្នន័យរួចហើយ',
    ],

    'record_not_found': [
        'Record not found',
        'រកមិនឃើញទិន្នន័យ',
    ],

    'user_not_found': [
        'User not found',
        'រកមិនឃើញអ្នកប្រើ',
    ],

    'employee_not_found': [
        'Employee not found',
        'រកមិនឃើញបុគ្គលិក',
        '未找到员工'
    ],

    'staff_not_found': [
        'Staff not found',
        'រកមិនឃើញបុគ្គលិក',
    ],

    'department_not_found': [
        'Department not found',
        'រកមិនឃើញនាយកដ្ឋាន',
    ],

    'position_not_found': [
        'Position not found',
        'រកមិនឃើញមុខតំណែង',
    ],

    'company_not_found': [
        'Company not found',
        'រកមិនឃើញក្រុមហ៊ុន',
    ],

    'branch_not_found': [
        'Branch not found',
        'រកមិនឃើញសាខា',
    ],

    'role_not_found': [
        'Role not found',
        'រកមិនឃើញតួនាទី',
    ],

    'asset_not_found': [
        'Asset not found',
        'រកមិនឃើញទ្រព្យសម្បត្តិ',
    ],

    'product_not_found': [
        'Product not found',
        'រកមិនឃើញផលិតផល',
    ],

    'merchant_not_found': [
        'Merchant not found',
        'រកមិនឃើញពាណិជ្ជករ',
    ],

    'account_disabled': [
        'Account disabled',
        'គណនីត្រូវបានបិទ',
    ],

    'tenant_suspended': [
        'This company account is suspended',
        'គណនីក្រុមហ៊ុននេះត្រូវបានផ្អាក',
    ],

    'tenant_not_found': [
        'This company account no longer exists',
        'គណនីក្រុមហ៊ុននេះលែងមានទៀតហើយ',
    ],

    'account_blocked': [
        'Account blocked',
        'គណនីត្រូវបានរារាំង',
    ],

    'unauthorized_access': [
        'Access denied',
        'គ្មានសិទ្ធិចូលប្រើ',
    ],

    'logout_success': [
        'Logged out successfully',
        'ចាកចេញដោយជោគជ័យ',
    ],
}

def get_translation(key: str) -> str:
    # Unknown keys fall back to the key itself (never raise); entries
    # missing a language fall back to English.
    entry = translations.get(key)
    if not entry:
        return key
    index = get_lang()
    return entry[index] if index < len(entry) else entry[0]
