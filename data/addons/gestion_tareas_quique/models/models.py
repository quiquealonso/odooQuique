from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class tareas_quique(models.Model):
    _name = 'gestion_tareas_quique.tareas_quique'
    _description = 'gestion_tareas_quique.tareas_quique'

    codigo = fields.Char(
        compute="_get_codigo",
        string="Codigo"
        )

    nombre = fields.Char(
        string="Nombre", 
        required=True, 
        help="Introduzca el nombre de la tarea")

    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción de la tarea")

    fecha_creacion = fields.Date(
        string="Fecha Creación", 
        required=True, 
        help="Fecha en la que se dio de alta la tarea")

    fecha_ini = fields.Datetime(
        string="Fecha Inicio", 
        required=True, 
        help="Fecha y hora de inicio de la tarea")

    fecha_fin = fields.Datetime(
        string="Fecha Final", 
        help="Fecha y hora de finalización de la tarea")

    finalizado = fields.Boolean(
        string="Finalizado", 
        help="Indica si la tarea ha sido finalizada o no")
    
   # sprint = fields.Many2one(
    #    'gestion_tareas_quique.sprints_quique', 
     #   string='Sprint relacionado', 
      #  ondelete='set null', 
       #    help='Sprint al que pertenece esta tarea')
    
    sprint = fields.Many2one(
        'gestion_tareas_quique.sprints_quique', 
        string='Sprint Activo', 
        compute='_compute_sprint', 
        store=True) 
    
    rel_tecnologias = fields.Many2many(
        comodel_name='gestion_tareas_quique.tecnologias_quique',
        relation='relacion_tareas_tecnologias',
        column1='rel_tareas',
        column2='rel_tecnologias',
        string='Tecnologías')
    
    historia = fields.Many2one(
        'gestion_tareas_quique.historias_quique', 
        string='historia de usuario', 
        ondelete='set null', 
        help='historia de usuario de la tarea')
    
    proyecto_ids = fields.Many2one(
        'gestion_tareas_quique.proyectos_quique',
        string='Proyecto',
        related='historia.proyecto',
        readonly=True)
        
    
    @api.depends('sprint', 'sprint.name')   # solo se ejecuta si cambia el sprint.
    def _get_codigo(self):
        _logger.info("Iniciando generación de códigos de tareas")

        for tarea in self:
            try:
                if not tarea.sprint:
                    _logger.warning(f"Tarea {tarea.id} sin sprint asignado")
                    tarea.codigo = "TSK_" + str(tarea.id)

                else:
                    # Si tiene sprint, usamos su nombre
                    tarea.codigo = str(tarea.sprint.name).upper() + "_" + str(tarea.id)

                _logger.debug(f"Código generado: {tarea.codigo}")

            except Exception as e:
                _logger.error(f"Error generando código para tarea {tarea.id}: {str(e)}")
                raise ValidationError(f"Error al generar el código: {str(e)}")

    @api.depends('historia', 'historia.proyecto')
    def _compute_sprint(self):
        for tarea in self:
            tarea.sprint = False

            # Verificar que la tarea tiene historia y proyecto
            if tarea.historia and tarea.historia.proyecto:
                # Buscar sprints del proyecto
                sprints = self.env['gestion_tareas_quique.sprints_quique'].search([
                    ('proyecto.id', '=', tarea.historia.proyecto.id)
                ])

                # Buscar el sprint activo (fecha_fin > ahora) 
                # de entre todos los sprints asociados al proyecto
                # en teoría solo hay un sprint activo, por eso es el que no ha vencido
                for sprint in sprints:
                    if (isinstance(sprint.fecha_fin, datetime) and 
                            sprint.fecha_ini <= datetime.now() and   
                            sprint.fecha_fin > datetime.now()):
                        tarea.sprint = sprint.id
                        break
class sprints_quique(models.Model):
    _name = 'gestion_tareas_quique.sprints_quique'
    _description = 'Modelo de Sprints para Gestión de Proyectos'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Introduzca el nombre del sprint")

    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción del sprint")

    fecha_ini = fields.Datetime(
        string="Fecha Inicio", 
        required=True, 
        help="Fecha y hora de inicio del sprint")
    duracion = fields.Integer(
        string="Duración", 
        help="Cantidad de días que tiene asignado el sprint")
    fecha_fin = fields.Datetime(
        compute='_compute_fecha_fin', 
        store=True,
        string="Fecha Fin")
    
    tareas = fields.One2many(
        'gestion_tareas_quique.tareas_quique', 
        'sprint', 
        string='Tareas del Sprint')
    
    proyecto = fields.Many2one(
        'gestion_tareas_quique.proyectos_quique', 
        string='proycto', 
        ondelete='set null', 
        help='proyecto asociado al srint'
    )
  
    @api.depends('fecha_ini', 'duracion')
    def _compute_fecha_fin(self):
        for sprint in self:
                if sprint.fecha_ini and sprint.duracion and sprint.duracion > -10:
                    sprint.fecha_fin = sprint.fecha_ini + timedelta(days=sprint.duracion)
                else:
                    sprint.fecha_fin = sprint.fecha_ini
   
            

    @api.constrains('fecha_ini', 'fecha_fin')
    def _check_fechas(self):
        for sprint in self:
            if sprint.fecha_fin and sprint.fecha_ini:
                if sprint.fecha_fin < sprint.fecha_ini:
                    raise ValidationError(
                        "La fecha de fin no puede ser anterior a la fecha de inicio."
                    )
class tecnologias_quique(models.Model):
    _name = 'gestion_tareas_quique.tecnologias_quique'
    _description = 'Modelo de Tecnologías'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Nombre de la tecnología")

    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción de la tecnología")

    logo = fields.Image(
        string="Logo", 
        max_width=256, 
        max_height=256,
        help="Logo de la tecnología")

    rel_tareas = fields.Many2many(
        comodel_name='gestion_tareas_quique.tareas_quique',
        relation='relacion_tareas_tecnologias',
        column1='rel_tecnologias',
        column2='rel_tareas',
        string='Tareas')

class proyectos_quique(models.Model):
    _name = 'gestion_tareas_quique.proyectos_quique'
    _description = 'Modelo de Proyectos para Gestión de Proyectos'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Introduzca el nombre del proyecto")

    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción del proyecto")
    
    
    historias = fields.One2many(
        'gestion_tareas_quique.historias_quique', 
        'proyecto', 
        string='Historias de usuario del proyecto')

class historias_quique(models.Model):
    _name = 'gestion_tareas_quique.historias_quique'
    _description = 'Modelo de Historias para Gestión de Proyectos'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Introduzca el nombre de la historia")

    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción de la historia")
    
    proyecto = fields.Many2one(
        'gestion_tareas_quique.proyectos_quique', 
        string='Proyecto al que pertenece la historia', 
        ondelete='set null', 
        help='Sprint al que pertenece esta tarea')
    
    tareas = fields.One2many(
        'gestion_tareas_quique.tareas_quique', 
        'historia', 
        string='Tareas de las historia')
    
    tecnologias = fields.Many2many(
        "gestion_tareas_quique.tecnologias_quique", 
        compute="_compute_tecnologias", 
        string="Tecnologías Utilizadas")

    @api.depends('tareas', 'tareas.rel_tecnologias')
    def _compute_tecnologias(self):
        for historia in self:
            tecnologias_acumuladas = self.env['gestion_tareas_quique.tecnologias_quique']

            # Recorrer todas las tareas de la historia
            for tarea in historia.tareas:
                # Sumar (concatenar) tecnologías de cada tarea
                tecnologias_acumuladas = tecnologias_acumuladas + tarea.rel_tecnologias

            # Asignar el resultado
            historia.tecnologias = tecnologias_acumuladas

    

    
