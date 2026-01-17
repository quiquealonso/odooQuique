from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger(__name__)



# MODELO PLATOS -----------------------------------------------------------------------
class platos_quique(models.Model):      
     _name = 'gest_rest.platos_quique'
     _description = 'gest_rest.platos_quique'

     name = fields.Char(
          string='Nombre del plato',
          required=True,
          help='Nombre del plato que se ofrece en el restaurante'
     )

     description = fields.Text(
          string='Descripcion del plato',
          required=True,
          help='Descripcion del plato que se ofrece en el restaurante'
     )

     precio = fields.Float(
          string='Precio del plato',
          required=True,
          help='Precio del plato que se ofrece en el restaurante'
     )

     disponible = fields.Boolean(
          default=True
     )
    
     tiempo_preparacion = fields.Integer(
          string='Tiempo de preparación del plato',
          required=True,
          help='Tiempo que tarda el plato en ser cocinado'
     )

     descuento = fields.Float(
          string='Descuento (%)',
     )
      

     # CAMPOS COMPUTADOS  -----------------------------------------------------------
     precio_final = fields.Float(
             string='Precio final del plato',
             store=True,
             compute='compute_precio_final',
          )
     precio_con_iva = fields.Float(
               compute="_compute_precio_con_iva",
               string="Precio con IVA"
          )
     codigo = fields.Char(
               compute="_get_codigo",
               string="Codigo"
          )
     
     

     # CAMPOS RELACIONADOS ---------------------------------------------------------
     menu = fields.Many2one(
          'gest_rest.menu_quique',
          ondelete='set null',
     )

     categoria_ids = fields.Many2one(
          'gest_rest.categoria_quique',
          string='Categoría del plato',
          ondelete='set null',
     )

     chef_ids = fields.Many2one(
          'gest_rest.chef_quique',
          ondelete='set null',
     )

     ingredientes = fields.Many2many(
          comodel_name='gest_rest.ingrediente_quique',
          relation='Relacion_ingrediente_plato',
          column1='plato_id',         
          column2='ingrediente_id',
          string='Platos que contienen este ingrediente'
     )

     chef_especializado = fields.Many2one(
          'gest_rest.chef_quique',
          string='Chef especializado',
          compute='_compute_chef_especializado',
          store=True
     )

     especialidad_chef = fields.Many2one(
          'gest_rest.categoria_quique',
          string='Especialidad del chef',
          related='chef_ids.especialidad_ids',
          readonly=True,
          store=False,
          help='Especialidad del chef asignado a este plato'
     )

     @api.depends('categoria_ids')
     def _compute_chef_especializado(self):
          for plato in self:
               plato.chef_especializado = False
               if plato.categoria_ids:
                    chef = self.env['gest_rest.chef_quique'].search([
                         ('especialidad_ids', '=', plato.categoria_ids.id)], limit=1)
                    if chef:
                         plato.chef_especializado = chef.id


     # METODOS ---------------------------------------------------------------------
     #------------------------------------------------------------------------------
     @api.depends('categoria_ids')
     def _get_codigo(self):
        for plato in self:
          try:
                    # Si la tarea no tiene categoria asignada
               if not plato.categoria_ids:
                    plato.codigo = "PLT" + str(plato.id)
                    _logger.warning(f"Plato {plato.id} sin categoría asignada")
               else:
                    # Si tiene categoria, usamos su nombre
                    plato.codigo = plato.categoria_ids.name[:3].upper() + "" + str(plato.id)
                    _logger.debug(f"Código generado: {plato.codigo}")
          except Exception as e:
                _logger.error(f"Error generando código para plato {plato.id}: {str(e)}")
                raise ValidationError(f"Error al generar el código: {str(e)}")
     
     # DEPENDS --------------------------------------------------------------------
     @api.depends('precio')
     def _compute_precio_con_iva(self):
          for plato in self:
               if plato.precio:
                    plato.precio_con_iva = plato.precio * 1.10
               else:
                    plato.precio_con_iva = 0.0
     @api.depends('precio_con_iva', 'descuento')
     def compute_precio_final(self):
          for plato in self:
               if plato.precio:
                    descuento_decimal = (plato.descuento or 0.0) / 100.0
                    if plato.descuento:
                         plato.precio_final = plato.precio * (1 - descuento_decimal)
                    else:
                         plato.precio_final = plato.precio
               else:
                    plato.precio_final = 0.0
     # CONSTRAINS ------------------------------------------------------------------
     @api.constrains('precio')
     def _precio_positivo(self):
          for plato in self:
               if plato.precio <= 0:
                    raise ValidationError('El precio tiene q ser mayor de 0.')
               _logger.info(f"Precio validado correctamente")

     @api.constrains('tiempo_preparacion')
     def _comprobar_tiempo(self):
          for plato in self:
               if plato.tiempo_preparacion:
                    if plato.tiempo_preparacion < 1 or plato.tiempo_preparacion > 240:
                         raise ValidationError('El tiempo del cocinado tiene que ser entre 1 minuto y 4 horas')

# MODELO MENÚ -----------------------------------------------------------------------
class menu_quique(models.Model):
     _name = 'gest_rest.menu_quique'
     _description = 'gest_rest.menu_quique'

     name = fields.Char(
          string='Nombre del menú',
          required=True,
          help='Nombre del menú que se ofrece en el restaurante'
     )

     description = fields.Text(
          string='Descripcion del menú',
          required=True,
          help='Descripcion del menú que se ofrece en el restaurante'
     )

     fecha_inicio = fields.Date(
          string='Fecha inicio del menú',
          help='Platos incluidos en este menú'
     )

     fecha_fin = fields.Date(
          string='Fecha de fin del menú',
          required=True,
          help='Fecha en la que este menú deja de estar disponible'
     )

     activo = fields.Boolean(
          default=True
     )

     # CAMPO RELACIONADO ---------------------------------------------------------
     platos = fields.One2many(
          'gest_rest.platos_quique',
          'menu',
          string='Platos del menú'
     )
     # CAMPO COMPUTADO -----------------------------------------------------------
     precio_total = fields.Float(
          string='Precio total',
          store=True,
          compute='_compute_precio_total',
     )
     
     # METODOS --------------------------------------------------------------------
     #-----------------------------------------------------------------------------


     # DEPENDS --------------------------------------------------------------------
     @api.depends('platos', 'platos.precio_final')
     def _compute_precio_total(self):
          for menu in self:
               precios = menu.platos.mapped('precio_final')
               menu.precio_total = sum(precios)

     # CONSTRAINS --------------------------------------------------------------------
     @api.constrains('fecha_inicio','fecha_fin')
     def _validar_fecha(self):
          for menu in self:
               if menu.fecha_fin:
                    if menu.fecha_fin < menu.fecha_inicio:
                         raise ValidationError('La fecha_fin no puede ser antes que la fecha_inicio.')
     
     @api.constrains('platos', 'activo')
     def _platos_menu(self):
          for menu in self:
               if menu.activo:
                    if len(menu.platos) == 0:
                         raise ValidationError('Un menú activo debe tener al menos un plato.')
                    



     

# MODELO INGREDIENTES -----------------------------------------------------------------------               
class ingrediente_quique(models.Model):
     _name = 'gest_rest.ingrediente_quique'
     _description = 'gest_rest.ingrediente_quique'

     name = fields.Char(
          string='Nombre del ingrediente',
          required=True,
          help='Nombre del ingrediente utilizado en los platos'
     )

     description = fields.Text(
          string='Descripcion del ingrediente',
          required=True,
          help='Descripcion del ingrediente utilizado en los platos'
     )

     es_alergeno = fields.Boolean(
          string='¿Es un alérgeno?',
          help='Indica si el ingrediente es un alérgeno común'
     )

     # CAMPO RELACIONADO ---------------------------------------------------------
     platos = fields.Many2many(
          comodel_name='gest_rest.platos_quique',
          relation='Relacion_ingrediente_plato',
          column1='ingrediente_id',
          column2='plato_id',
          string='Platos que contienen este ingrediente'
     )

     categoria_ids = fields.Many2many(
          comodel_name='gest_rest.categoria_quique',
          relation='relacion_categoria_ingrediente',
          column1='ingrediente_id',
          column2='categoria_id',
          string='Categorías relacionadas',
          help='Categorías a las que pertenece este ingrediente'
     )
     
class categoria_quique(models.Model):

          
     _name = 'gest_rest.categoria_quique'
     _description = 'gest_rest.categoria_quique'
     name = fields.Char(
          string='Nombre de la categoría',
          required=True,
     )   

     descripcion = fields.Text(
          string='Descripción de la categoría',
     )

     chef_ids = fields.One2many(
          'gest_rest.chef_quique',
          'especialidad_ids',
          string='Chef de la categoría',
     )
     platos_ids = fields.One2many(
          'gest_rest.platos_quique',
          'categoria_ids',
          string='Platos de la categoría'
     )

     ingredientes_comunes = fields.Many2many(
          'gest_rest.ingrediente_quique',
          string='Ingredientes comunes',
          compute='_compute_ingredientes_comunes'
     )

     @api.depends('platos_ids', 'platos_ids.ingredientes')
     def _compute_ingredientes_comunes(self):
          for categoria in self:
               acumulado = self.env['gest_rest.ingrediente_quique'].browse([])
               for plato in categoria.platos_ids:
                    acumulado = acumulado + plato.ingredientes
               categoria.ingredientes_comunes = acumulado


class chef_quique(models.Model):
     _name = 'gest_rest.chef_quique'
     _description = 'gest_rest.chef_quique'
     name = fields.Char(
          string='Nombre del chef',
          required=True,
     )   

     especialidad_ids = fields.Many2one(
          'gest_rest.categoria_quique',
          string='Especialidad del chef',
     )

     platos_asignados = fields.One2many(
          'gest_rest.platos_quique',
          'chef_ids',
          string='Platos asignados al chef'
     )