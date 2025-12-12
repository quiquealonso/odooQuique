# from odoo import http


# class GestionRestauranteQuique(http.Controller):
#     @http.route('/gestion_restaurante_quique/gestion_restaurante_quique', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_restaurante_quique/gestion_restaurante_quique/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_restaurante_quique.listing', {
#             'root': '/gestion_restaurante_quique/gestion_restaurante_quique',
#             'objects': http.request.env['gestion_restaurante_quique.gestion_restaurante_quique'].search([]),
#         })

#     @http.route('/gestion_restaurante_quique/gestion_restaurante_quique/objects/<model("gestion_restaurante_quique.gestion_restaurante_quique"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_restaurante_quique.object', {
#             'object': obj
#         })

