from datetime import timedelta
from odoo import models, fields, api


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
    
    sprint = fields.Many2one(
        'gestion_tareas_quique.sprints_quique', 
        string='Sprint relacionado', 
        ondelete='set null', 
        help='Sprint al que pertenece esta tarea')
    
    rel_tecnologias = fields.Many2many(
        comodel_name='gestion_tareas_quique.tecnologias_quique',
        relation='relacion_tareas_tecnologias',
        column1='rel_tareas',
        column2='rel_tecnologias',
        string='Tecnologías')

    def _get_codigo(self):
        for tarea in self:
            # Si la tarea no tiene un sprint asignado
            if not tarea.sprint:
                tarea.codigo = "TSK_" + str(tarea.id)
            else:
             # Si tiene sprint, usamos su nombre
                tarea.codigo = str(tarea.sprint.name).upper() + "_" + str(tarea.id)

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
  
    @api.depends('fecha_ini', 'duracion')
    def _compute_fecha_fin(self):
        for sprint in self:
            if sprint.fecha_ini and sprint.duracion and sprint.duracion > 0:
                sprint.fecha_fin = sprint.fecha_ini + timedelta(days=sprint.duracion)
            else:
                sprint.fecha_fin = sprint.fecha_ini
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

