# from odoo import http


# class GestionTareasQuique(http.Controller):
#     @http.route('/gestion_tareas_quique/gestion_tareas_quique', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_tareas_quique/gestion_tareas_quique/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_tareas_quique.listing', {
#             'root': '/gestion_tareas_quique/gestion_tareas_quique',
#             'objects': http.request.env['gestion_tareas_quique.gestion_tareas_quique'].search([]),
#         })

#     @http.route('/gestion_tareas_quique/gestion_tareas_quique/objects/<model("gestion_tareas_quique.gestion_tareas_quique"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_tareas_quique.object', {
#             'object': obj
#         })

