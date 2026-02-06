from odoo import models, fields, api
from .logica_dronify import calcular_consumo_vuelo, validar_estado_bateria
from datetime import datetime

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

    #####################CAMPOS RELACIONADOS#########################

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
        string="Capacidad Máxima",
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

    #####################CAMPOS RELACIONADOS#########################
    #Pilotos certificados para este dron (relación inversa)
    piloto_autorizado_ids = fields.Many2many(
        'res.partner',
        string="Pilotos Autorizados",
        domain=[('es_piloto', '=', True)],
    )


    #relacion con el paquete
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
   
    #####################CAMPOS RELACIONADOS#########################
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

    #####################CAMPOS RELATED#########################

    #Nombre del dron del vuelo(campo Related, solo lectura )
    dron_relacionado = fields.Char(
        string="Dron del Vuelo",
        related='vuelo_id.dron_id.name',
        readonly=True,
    )



class dronify_qap_vuelo(models.Model):
    _name = 'dronify_qap_vuelo'
    _description = 'dronify_qap_vuelo'

    #Código único del vuelo
    codigo = fields.Char(
        string="Código Vuelo",
        default=datetime.now().strftime("%Y%m%d%H%M%S"),
        readonly=True,
        store=True,
    )

    #Denominación de la misión
    name = fields.Char(
        string="Denominación de la misión",
        default=datetime.now().strftime("%Y-%m-%d_Vuelo"),
        required=True,
        store=True,
    )

    #Indica si el vuelo está listo para ejecutarse
    preparado = fields.Boolean(
        string="Preparado para despegue",
        store=True,
    )

    #Indica si el vuelo se ha completado
    realizado = fields.Boolean(
        string="Vuelo realizado",
        store=True,
    )

    #dron asignado
    dron_id = fields.Many2one(
        'dronify_qap_dron',
        string="Dron Asignado",
        required=True,
        store=True,
    )

    #####################CAMPOS RELACIONADOS#########################
    #piloto asignado
    piloto_id = fields.Many2one(
        'res.partner',
        string="Piloto Asignado",
        required=True,
        domain=[('es_piloto', '=', True)],
        store=True,
    )

    #paquetes a transportar
    paquetes_ids = fields.One2many(
        'dronify_qap_paquete',
        'vuelo_id',
        string="Paquetes Asignados",
        store=True,
    )

    
    #####################CAMPOS COMPUTADOS#########################
    #Suma del peso de todos los paquetes asignados (campo computado)
    peso_total = fields.Float(
        string="Peso Total (kg)",
        compute='_compute_peso_total',
        store=True,
    )

    #Porcentaje de batería que consumirá el vuelo (campo computado)
    consumo_estimado = fields.Float(
        string="Consumo Estimado (%)",
        #compute='calcular_consumo_vuelo',
        store=True,
        #este campo va a utilziar un campo computado que va a utilizar el metodo del logica_dronify
    )

    @api.depends('paquetes_ids.peso')
    def _compute_peso_total(self):
        for vuelo in self:
            vuelo.peso_total = sum(paquete.peso for paquete in vuelo.paquetes_ids)

    

    







