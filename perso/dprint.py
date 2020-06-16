from pprint import pprint
from collections import OrderedDict
import traceback


def dprint(rec=None, section=None, obj=None, field=None, trace=None, applycondition=False, force_print=False):
    to_print = OrderedDict()
    ok = []

    condition = rec and rec._name in ['product.product', 'product.template', 'sale.order.line']
    _apply = applycondition and condition

    def add_key(key, value):
        ok.append(key)
        to_print[key] = value

    to_print['section'] = section.upper()
    to_print['fname'] = field
    if condition:
        if field and field in rec._fields:
            add_key('field_value', rec[field])
    if obj:
        add_key('obj', obj)
    if trace:
        add_key('trace', traceback.format_stack(limit=20))
    if ok and (not applycondition or _apply) or force_print:
        pprint(to_print)

def test_new_lead_from_email_multicompany(object0):
    self = object0
    companies = self.env['res.company'].search([])

    company0 = companies[0]
    company1 = companies[1]
    self.env.user.write({
        'company_ids': [(4, company0.id, False), (4, company1.id, False)],
    })

    crm_team_model = self.env['ir.model'].search([('model', '=', 'crm.team')])
    crm_lead_model = self.env['ir.model'].search([('model', '=', 'crm.lead')])
    self.env["ir.config_parameter"].sudo().set_param("mail.catchall.domain", 'aqualung.com')

    crm_team0 = self.env['crm.team'].create({
        'name': 'crm team 0',
        'company_id': company0.id,
    })
    crm_team1 = self.env['crm.team'].create({
        'name': 'crm team 1',
        'company_id': company1.id,
    })

    mail_alias0 = self.env['mail.alias'].create({
        'alias_name': 'sale_team_0',
        'alias_model_id': crm_lead_model.id,
        'alias_parent_model_id': crm_team_model.id,
        'alias_parent_thread_id': crm_team0.id,
        'alias_defaults': "{'type': 'opportunity', 'team_id': %s}" % crm_team0.id,
    })
    mail_alias1 = self.env['mail.alias'].create({
        'alias_name': 'sale_team_1',
        'alias_model_id': crm_lead_model.id,
        'alias_parent_model_id': crm_team_model.id,
        'alias_parent_thread_id': crm_team1.id,
        'alias_defaults': "{'type': 'opportunity', 'team_id': %s}" % crm_team1.id,
    })

    crm_team0.write({'alias_id': mail_alias0.id})
    crm_team1.write({'alias_id': mail_alias1.id})

new_message0 = """MIME-Version: 1.0
Date: Thu, 27 Dec 2018 16:27:45 +0100
Message-ID: blablabla055
Subject: sale team 0 in company 0
From:  A client <client_a@someprovider.com>
To: lool2@lpe.com
Content-Type: multipart/alternative; boundary="000000000000a47519057e029630"

--000000000000a47519057e029630
Content-Type: text/plain; charset="UTF-8"


--000000000000a47519057e029630
Content-Type: text/html; charset="UTF-8"
Content-Transfer-Encoding: quoted-printable

<div>A good message</div>

--000000000000a47519057e029630--
"""

new_message1 = """MIME-Version: 1.0
Date: Thu, 27 Dec 2018 16:27:45 +0100
Message-ID: blablabla1
Subject: sale team 1 in company 1
From:  B client <client_b@someprovider.com>
To: sale_team_1@aqualung.com
Content-Type: multipart/alternative; boundary="000000000000a47519057e029630"

--000000000000a47519057e029630
Content-Type: text/plain; charset="UTF-8"


--000000000000a47519057e029630
Content-Type: text/html; charset="UTF-8"
Content-Transfer-Encoding: quoted-printable

<div>A good message bis</div>

--000000000000a47519057e029630--
"""


def lol(lines):
    for line in lines['lines']:
        col_index = 0
        for col in line['columns']:
            lines.get('columns_header')[col_index + line.get('colspan', 1)]
            col_index += 1

def pack_lines(lines, _print=True):
    packed = [(l.balance, l.amount_currency, l.amount_residual, l.amount_residual_currency, l.account_id.name) for l in lines]
    if _print:
        pprint(packed)
    else:
        return packed
