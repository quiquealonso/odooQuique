# from odoo import http


# class DronifyQuique(http.Controller):
#     @http.route('/dronify_quique/dronify_quique', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dronify_quique/dronify_quique/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dronify_quique.listing', {
#             'root': '/dronify_quique/dronify_quique',
#             'objects': http.request.env['dronify_quique.dronify_quique'].search([]),
#         })

#     @http.route('/dronify_quique/dronify_quique/objects/<model("dronify_quique.dronify_quique"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dronify_quique.object', {
#             'object': obj
#         })

