from odoo import models, fields, api


class dronify_qap_dron(models.Model):
    _name = 'dronify_quique.dronify_quique'
    _description = 'dronify_quique.dronify_quique'

    #Nombre identificativo del dron
    name = fields.Char()
    capacidad_max = fields.Float(
        required=True
    )

    #Nivel de carga actual (0-100%)
    bateria = fields.Integer(
        default=100,
        string="Batería",
    )

   
    #Estado operativo del dron
    estado = fields.Selection(
        [('disponible', 'Disponible'),
          ('vuelo', 'Vuelo'),
          ('taller', 'NoTallerche')],
          string='Estado dron',
          default='disponible'
    )

    #Pilotos certificados para este dron (relación inversa)
    #piloto_autorizado_ids = fields.Many2many()

     

class dronify_qap_vuelo(models.Model):
    _name = 'dronify_qap_vuelo'
    _description = 'dronify_qap_vuelo'

    #Código único del vuelo
    codigo = fields.Char(
        required=True,
        string="Código Vuelo",
        readonly=True,
    )

    name = fields.Char(
        string="Denominación de la misión",
       # default=datetime.now().strftime("Vuelo %Y-%m-%d %H:%M:%S"),
       required=True,
    )

    #dron asignado
    #dron_id = fields.Many2one(

    preparado = fields.Boolean(
        string="Preparado para despegue",
    )

    realizado = fields.Boolean(
        string="Vuelo realizado",
    )


class dronify_qap_paquete(models.Model):
    _name = 'dronify_qap_paquete'
    _description = 'dronify_qap_paquete'

    #Identificador único
    codigo = fields.Char(
        required=True,
        string="Código Paquete",
        readonly=True,
    )
 
    #Descripción del contenido
    name = fields.Char(
        string="Descripción",
        required=True,
    )

    #Peso en kilogramos
    peso = fields.Float(
        string="Peso (kg)",
        required=True,
    )

    #Cliente que envía el paquete
    #cliente_id = fields.Many2one()

    #Vuelo asignado
    #vuelo_id = fields.Many2one()
       
    #Nombre del dron del vuelo
    #dron_relacionado = fields.Char()


# class dronify_qap_contactos(models.Model):
#     _name = 'res.partner'
#     _inherit = 'res.partner'

#     #Identifica si el contacto es cliente
#     es_cliente = fields.Boolean(string="Es Cliente")

#     #Marca clientes premium (activa modo ahorro en vuelos)
#     es_vip = fields.Boolean(string="Es vip")

#     #Identifica si el contacto es piloto
#     es_piloto = fields.Boolean(string="Es Piloto")

#     #Número de licencia del piloto (obligatorio solo para pilotos)
#     licencia = fields.Char(string="Licencia de Piloto")

