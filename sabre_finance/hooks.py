app_name = "sabre_finance"
app_title = "Sabre Finance"
app_publisher = "Main Telecom"
app_description = "Sabre Financial Workflow Management"
app_email = "m.raed@cx3.me"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "sabre_finance",
# 		"logo": "/assets/sabre_finance/logo.png",
# 		"title": "Sabre Finance",
# 		"route": "/sabre_finance",
# 		"has_permission": "sabre_finance.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sabre_finance/css/sabre_finance.css"
# app_include_js = "/assets/sabre_finance/js/sabre_finance.js"

# include js, css files in header of web template
# web_include_css = "/assets/sabre_finance/css/sabre_finance.css"
# web_include_js = "/assets/sabre_finance/js/sabre_finance.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sabre_finance/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "sabre_finance/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "sabre_finance.utils.jinja_methods",
# 	"filters": "sabre_finance.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "sabre_finance.install.before_install"
# after_install = "sabre_finance.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "sabre_finance.uninstall.before_uninstall"
# after_uninstall = "sabre_finance.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "sabre_finance.utils.before_app_install"
# after_app_install = "sabre_finance.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "sabre_finance.utils.before_app_uninstall"
# after_app_uninstall = "sabre_finance.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sabre_finance.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"sabre_finance.tasks.all"
# 	],
# 	"daily": [
# 		"sabre_finance.tasks.daily"
# 	],
# 	"hourly": [
# 		"sabre_finance.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sabre_finance.tasks.weekly"
# 	],
# 	"monthly": [
# 		"sabre_finance.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "sabre_finance.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "sabre_finance.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sabre_finance.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "sabre_finance.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["sabre_finance.utils.before_request"]
# after_request = ["sabre_finance.utils.after_request"]

# Job Events
# ----------
# before_job = ["sabre_finance.utils.before_job"]
# after_job = ["sabre_finance.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"sabre_finance.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []


fixtures = [
    {
        "doctype": "DocType",
        "filters": [["module", "=", "Sabre Finance"]]
    }
]

fixtures += [
    {
        "doctype": "Workflow",
        "filters": [["document_type", "=", "Payment Tracking"]]
    },
    {
        "doctype": "Workflow State",
        "filters": [["name", "in", ["Draft", "Pending Account Manager Review", "Pending Neveen Review", "Pending Agency Claim", "Pending Finance Review", "Approved", "Rejected"]]]
    },
    {
        "doctype": "Workflow Action Master",
        "filters": [["name", "in", ["Send for Review", "Approve", "Claim Submitted", "Transfer Done"]]]
    },
    {
        "doctype": "Role",
        "filters": [["name", "in", ["Sabre Finance", "Sabre Account Manager", "Sabre Finance Manager"]]]
    }
]

fixtures += [
    {
        "doctype": "Notification",
        "filters": [["document_type", "=", "Payment Tracking"]]
    }
]

fixtures += [
    {
        "doctype": "Server Script",
        "filters": [["module", "=", "Sabre Finance"]]
    },
    {
        "doctype": "Server Script",
        "filters": [["name", "in", [
            "Generate Measurement Calculation",
            "Generate Payment Schedule",
            "Auto Calculate Term and Payment Schedule"
        ]]]
    }
]

fixtures += [
    {
        "doctype": "Custom DocPerm",
        "filters": [["parent", "in", ["Agency Contract", "Segment Report", "Booking Measurement", "Payment Tracking", "Frontline Incentive"]]]
    }
]

fixtures += [
    {
        "doctype": "Client Script",
        "filters": [["module", "=", "Sabre Finance"]]
    }
]

fixtures += [
    {
        "doctype": "Dashboard",
        "filters": [["module", "=", "Sabre Finance"]]
    },
    {
        "doctype": "Number Card",
        "filters": [["module", "=", "Sabre Finance"]]
    },
    {
        "doctype": "Dashboard Chart",
        "filters": [["module", "=", "Sabre Finance"]]
    }
]

fixtures += [
    {
        "doctype": "Print Format",
        "filters": [["module", "=", "Sabre Finance"]]
    }
]
fixtures += [
    {
        "doctype": "Workspace",
        "filters": [["module", "=", "Sabre Finance"]]
    },
    {
        "doctype": "Workspace Sidebar",
        "filters": [["app", "=", "sabre_finance"]]
    },
    {
        "doctype": "Report", 
        "filters": [["module", "=", "Sabre Finance"]]
    },
    {
        "doctype": "Custom HTML Block",
        "filters": [["name", "in", ["Chart For Payment In Month"]]]
    }
]
after_migrate = ["sabre_finance.setup.import_workspace"]

fixtures += [
    {
        "doctype": "Custom Field",
        "filters": [["module", "=", "Sabre Finance"]]
    },
    {
        "doctype": "Property Setter",
        "filters": [["module", "=", "Sabre Finance"]]
    }
]
