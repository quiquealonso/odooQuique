# from odoo import http


# class Gest-rest(http.Controller):
#     @http.route('/gest-rest/gest-rest', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gest-rest/gest-rest/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gest-rest.listing', {
#             'root': '/gest-rest/gest-rest',
#             'objects': http.request.env['gest-rest.gest-rest'].search([]),
#         })

#     @http.route('/gest-rest/gest-rest/objects/<model("gest-rest.gest-rest"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gest-rest.object', {
#             'object': obj
#         })

