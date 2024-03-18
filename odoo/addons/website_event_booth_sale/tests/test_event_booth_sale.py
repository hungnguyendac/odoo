# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta

from odoo import Command, fields
from odoo.addons.website_event_sale.tests.common import TestWebsiteEventSaleCommon
from odoo.addons.base.tests.common import HttpCaseWithUserPortal
from odoo.tests.common import tagged



@tagged('post_install', '-at_install')
class TestWebsiteEventBoothSale(HttpCaseWithUserPortal, TestWebsiteEventSaleCommon):

    def setUp(self):
        super().setUp()
        self.env['ir.config_parameter'].sudo().set_param('account.show_line_subtotals_tax_selection', 'tax_included')
        self.tax = self.env['account.tax'].sudo().create({
            'name': 'Tax 10',
            'amount': 10,
        })
        self.booth_product = self.env['product.product'].create({
            'name': 'Test Booth Product',
            'description_sale': 'Mighty Booth Description',
            'list_price': 20,
            'standard_price': 60.0,
            'taxes_id': [(6, 0, [self.tax.id])],
            'detailed_type': 'event_booth',
        })
        self.event_booth_category = self.env['event.booth.category'].create({
            'name': 'Standard',
            'description': '<p>Standard</p>',
            'product_id': self.booth_product.id,
            'price': 100.0,
        })
        self.event_type = self.env['event.type'].create({
            'name': 'Booth Type',
            'event_type_booth_ids': [
                Command.create({
                    'name': 'Standard 1',
                    'booth_category_id': self.event_booth_category.id,
                }),
                Command.create({
                    'name': 'Standard 2',
                    'booth_category_id': self.event_booth_category.id,
                }),
                Command.create({
                    'name': 'Standard 3',
                    'booth_category_id': self.event_booth_category.id,
                }),
            ],
        })
        self.env['event.event'].create({
            'name': 'Test Event Booths',
            'event_type_id': self.event_type.id,
            'date_begin': fields.Datetime.to_string(datetime.today() + timedelta(days=1)),
            'date_end': fields.Datetime.to_string(datetime.today() + timedelta(days=15)),
            'website_published': True,
            'website_menu': True,
            'booth_menu': True,
        })

    def test_tour(self):
        self.partner_portal.write({
            'street': '858 Lynn Street',
            'city': 'Bayonne',
            'country_id': self.env.ref('base.state_us_25').id,
            'zip': '07002',
            'phone': '(683)-556-5104',
        })
        self.start_tour('/event', 'website_event_booth_tour', login='portal')

    def test_booth_pricelists_different_currencies(self):
        self.env.ref('base.user_admin').partner_id.write({
            'email': 'mitchell.stephen@example.com',
            'name': 'Mitchell Admin',
            'street': '215 Vine St',
            'city': 'Scranton',
            'zip': '18503',
            'country_id': self.env.ref('base.us').id,
            'state_id': self.env.ref('base.state_us_39').id,
            'phone': '+1 555-555-5555',
        })
        self.start_tour("/web", 'event_booth_sale_pricelists_different_currencies', login='admin')
