# -*- encoding: utf-8 -*-
##############################################################################
#
#    ServerPLM, Open Source Product Lifcycle Management System    
#    Copyright (C) 2020-2022 Didotech srl (<http://www.didotech.com>). All Rights Reserved
#    
#    Created on : 2022-09-23
#    Author : Fabio Colognesi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Extension for Purchase',
    'version': '1.0.0',
    'author': 'Didotech srl',
    'website': 'http://www.didotech.com',
    'support': 'support@didotech.com',
    'category': 'Document Management',
    'sequence': 10,
    'summary': 'PLM Engineering addition extending Purchase to attach pdf documents to "send a mail" feature.',
    'images': [],
    'depends': [
        'purchase',
        'pdm'
    ],
    'description': """
    """,
    'data': [
       ],
    'demo': [
        ],
    'test': [
        ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
