from odoo import models, fields, api


class dronify_qap_contactos(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    #Identifica si el contacto es cliente
    es_cliente = fields.Boolean(string="Es Cliente")

    #Marca clientes premium (activa modo ahorro en vuelos)
    es_vip = fields.Boolean(string="Es vip")

    #Identifica si el contacto es piloto
    es_piloto = fields.Boolean(string="Es Piloto")

    #Número de licencia del piloto (obligatorio solo para pilotos)
    licencia = fields.Char(string="Licencia de Piloto")

    #Lista de drones que el piloto está certificado para operar
    dron_autorizado_ids = fields.Many2many(
        'dronify_qap_dron',
        string="Drones Autorizados",
    )

    #relacion con los paquetes
    paquete = fields.One2many(
        'dronify_qap_paquete',
        'cliente_id',
        string="Paquetes Enviados",
    )


class dronify_qap_dron(models.Model):
    _name = 'dronify_qap_dron'
    _description = 'dronify_quique.dronify_quique'

    #Nombre identificativo del dron
    name = fields.Char(
        string = "nombre"
    )

    #Carga máxima en kilogramos(obligatorio)
    capacidad_max = fields.Float(
        required=True
    )

    #Nivel de carga actual (0-100%)
    bateria = fields.Integer(
        default=100,
        string="Batería",
    )
    #esto lo tenemos que limitar con una funcion o en la vista basta??

   
    #Estado operativo del dron
    estado = fields.Selection(
        [('disponible', 'Disponible'),
          ('vuelo', 'Vuelo'),
          ('taller', 'Taller')],
          string='Estado dron',
          default='disponible'
    )

    #Pilotos certificados para este dron (relación inversa)
    piloto_autorizado_ids = fields.Many2many(
        'res.partner',
        string="Pilotos Autorizados",
        domain=[('es_piloto', '=', True)],
    )

    paquete = fields.One2many(
        'dronify_qap_paquete',
        'vuelo_id',
        string="Paquetes Asignados",
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

    #Cliente que envía el paquete(al piloto) (obligado)
    cliente_id = fields.Many2one(
        'res.partner',
        string="Cliente Remitente",
        required=True,
        domain=[('es_cliente', '=', True)],
    )

    #Vuelo asignado (solo lectura)
    vuelo_id = fields.Many2one(
        'dronify_qap_vuelo',
        string="Vuelo Asignado",
        readonly=True,
    )

    #Nombre del dron del vuelo(campo Related, solo lectura Solo lectura)
   # dron_relacionado = fields.related()
       
    #Nombre del dron del vuelo
    #dron_relacionado = fields.Char()



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
    dron_id = fields.Many2one(
        'dronify_qap_dron',
        string="Dron Asignado",
        required=True,
    )

    #piloto asignado
    piloto_id = fields.Many2one(
        'res.partner',
        string="Piloto Asignado",
        required=True,
        domain=[('es_piloto', '=', True)],
    )

    #paquetes a transportar
    paquetes_ids = fields.One2many(
        'dronify_qap_paquete',
        'vuelo_id',
        string="Paquetes Asignados",
    )

    #Indica si el vuelo está listo para ejecutarse
    preparado = fields.Boolean(
        string="Preparado para despegue",
    )

    #Indica si el vuelo se ha completado
    realizado = fields.Boolean(
        string="Vuelo realizado",
    )

    #Suma del peso de todos los paquetes asignados (campo computado)
    #peso_total = fields.computed()

    #Porcentaje de batería que consumirá el vuelo (campo computado)
    #consumo_estimado = fields.computed()







