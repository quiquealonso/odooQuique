from odoo import models, fields, api
from odoo.exceptions import ValidationError
from .logica_dronify import calcular_consumo_vuelo, validar_estado_bateria
from datetime import datetime

class dronify_qap_contactos(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    #Identifica si el contacto es cliente
    es_cliente = fields.Boolean(string="¿Es Cliente?")

    #Marca clientes premium (activa modo ahorro en vuelos)
    es_vip = fields.Boolean(string="¿Es vip?")

    #Identifica si el contacto es piloto
    es_piloto = fields.Boolean(string="¿Es Piloto?")

    #Número de licencia del piloto (obligatorio solo para pilotos)
    licencia = fields.Char(
        string="Nº de licencia",
        requiered=es_piloto,
        
    )

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
        string = "Nombre del  Dron"
    )

    #Carga máxima en kilogramos(obligatorio)
    capacidad_max = fields.Float(
        string="Capacidad Carga (kg)",
        required=True
    )

    #Nivel de carga actual (0-100%)
    bateria = fields.Integer(
        default=100,
        string="Nivel de Batería (%)",
    )

   
    #Estado operativo del dron
    estado = fields.Selection(
        [('disponible', 'Disponible'),
          ('vuelo', 'Vuelo'),
          ('taller', 'Taller')],
          string='Estado',
          default='disponible'
    )

    #####################CAMPOS RELACIONADOS#########################
    #Pilotos certificados para este dron (relación inversa)
    piloto_autorizado_ids = fields.Many2many(
        'res.partner',
        string="Pilotos Autorizados",
        domain=[('es_piloto', '=', True)],
    )

    @api.constrains('bateria')
    def _check_bateria_rango(self):
        for dron in self:
            if dron.bateria < 0 or dron.bateria > 100:
                raise ValidationError("El nivel de batería debe estar entre 0 y 100%.")


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
        default=datetime.now().strftime("%Y%m%d%H%M%S"),
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
        string="Cliente",
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
        string="Vuelo preparado",
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
        compute='_compute_consumo_estimado',
        store=True,
    )

    @api.depends('paquetes_ids.peso')
    def _compute_peso_total(self):
        for vuelo in self:
            vuelo.peso_total = sum(paquete.peso for paquete in vuelo.paquetes_ids)

    # esto es preciso ?? 'paquetes_ids.cliente_id.es_vip'
    @api.depends('peso_total', 'paquetes_ids')
    def _compute_consumo_estimado(self):
        for vuelo in self:
            es_vip = any(vuelo.paquetes_ids.mapped('cliente_id.es_vip'))
            vuelo.consumo_estimado = calcular_consumo_vuelo(vuelo.peso_total, es_vip)




    #####################MÉTODOS DE ACCIÓN#########################
    def action_preparar_vuelo(self):
        for vuelo in self:
            #Debe tener dron y piloto asignados
            if not vuelo.dron_id:
                raise ValidationError("El vuelo debe tener un dron asignado.")
            if not vuelo.piloto_id:
                raise ValidationError("El vuelo debe tener un piloto asignado.")
            
            #Debe tener al menos un paquete asignado
            if not vuelo.paquetes_ids:
                raise ValidationError("El vuelo debe tener al menos un paquete asignado.")
            
            #El peso total no puede superar la capacidad máxima del dron
            if vuelo.peso_total > vuelo.dron_id.capacidad_max:
                raise ValidationError(
                    f"El peso total ({vuelo.peso_total} kg) supera la capacidad máxima del dron "
                    f"({vuelo.dron_id.capacidad_max} kg)."
                )      
            #El dron debe estar en estado 'disponible'
            if vuelo.dron_id.estado != 'disponible':
                raise ValidationError(
                    f"El dron '{vuelo.dron_id.name}' no está disponible. "
                    f"Estado actual: {dict(vuelo.dron_id._fields['estado'].selection).get(vuelo.dron_id.estado)}"
                )
            #La batería actual del dron debe ser mayor o igual al consumo estimado
            if vuelo.dron_id.bateria < vuelo.consumo_estimado:
                raise ValidationError(
                    f"Batería insuficiente. El dron tiene {vuelo.dron_id.bateria}% de batería "
                    f"pero el vuelo requiere {vuelo.consumo_estimado}%."
                )
            
            #El piloto debe tener el dron asignado en su lista de "Drones Autorizados"
            if vuelo.dron_id not in vuelo.piloto_id.dron_autorizado_ids:
                raise ValidationError(
                    f"El piloto '{vuelo.piloto_id.name}' no está certificado para operar el dron '{vuelo.dron_id.name}'."
                )
            

            #Todo normal:
            vuelo.preparado = True
            vuelo.dron_id.estado = 'vuelo'

    def action_desbloquear(self):
        for vuelo in self:
            if not vuelo.realizado:
                vuelo.preparado = False
                vuelo.estado_dron = 'disponible'

    def action_finalizar_vuelo(self):
        for vuelo in self:
            if vuelo.preparado:
                vuelo.realizado = True
                vuelo.dron_id.bateria -= vuelo.consumo_estimado
                vuelo.dron_id.estado = 'disponible'







