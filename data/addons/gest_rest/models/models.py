from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger(__name__)



# MODELO PLATOS -----------------------------------------------------------------------
class platos_quique(models.Model):
     _name = 'gest_rest.platos_quique'
     _description = 'gest_rest.platos_quique'

     name = fields.Char(
          String ='Nombre del plato',
          Required = True,
          help='Nombre del plato que se ofrece en el restaurante'
     )

     description = fields.Text(
          String ='Descripcion del plato',
          Required = True,
          help='Descripcion del plato que se ofrece en el restaurante'
     )

     precio = fields.Float(
          String ='Precio del plato',
          Required = True,
          help='Precio del plato que se ofrece en el restaurante'
     )

     disponible = fields.Boolean(
          default=True
     )
    
     tiempo_preparacion = fields.Integer(
          String ='Tiempo de preparación del plato',
          Required = True,
          help='Tiempo que tarda el plato en ser cocinado'
     )

     descuento = fields.Float(
          String ='Descuento (%)',
     )
     
     categoria = fields.Selection( 
     [('entrada', 'Entrada'),
      ('plato_principal', 'Plato Principal'),
      ('postre', 'Postre'),
      ('bebida', 'Bebida')],
     string='Categoría', 
     required=True,
     help='Categoría del plato en el menú del restaurante'
     )
    

     

     # CAMPOS COMPUTADOS  -----------------------------------------------------------
     precio_final = fields.Float(
          String ='Precio final del plato',
          store = True,
          compute = 'compute_precio_final',
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
     
     ingredientes = fields.Many2many(
          comodel_name='gest_rest.ingrediente_quique',
          relation='Relacion_ingrediente_plato',
          column1='plato_id',         
          column2='ingrediente_id',
          string='Platos que contienen este ingrediente'
     )
     # METODOS ---------------------------------------------------------------------
     #------------------------------------------------------------------------------
     def _get_codigo(self):
          try:
               for plato in self:
                    if not plato.menu:
                         plato.codigo = "TSK_" + str(plato.id)
                         _logger.debug(f"Codigo para plato sin menu: {plato.codigo}")
                    else:
                         if not plato.categoria:
                              _logger.warning(f"El plato '{plato.name}' no tiene categoría definida.")
                              raise ValidationError("No hay categoria para el plato.")
                         plato.codigo = plato.categoria[:3].upper() + "_" + str(plato.id)
                         _logger.debug(f"Codigo para plato con menu: {plato.codigo}")
          except Exception as e:
               _logger.error(f"Error al calcular el código del plato: {str(e)}")
               raise ValidationError(f"Error al calcular el codigo: {str(e)}")
     
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
          String ='Nombre del menú',
          Required = True,
          help='Nombre del menú que se ofrece en el restaurante'
     )

     description = fields.Text(
          String ='Descripcion del menú',
          Required = True,
          help='Descripcion del menú que se ofrece en el restaurante'
     )

     fecha_inicio = fields.Date(
          comodel_name='gest_rest.platos_quique',
          string='Fecha inicio del menú',
          help='Platos incluidos en este menú'
     )

     fecha_fin = fields.Date(
          String ='Fecha de fin del menú',
          Required = True,
          help='Fecha en la que este menú deja de estar disponible'
     )

     activo = fields.Boolean(
          default=True
     )

     # CAMPO RELACIONADO ---------------------------------------------------------
     platos = fields.One2many(
          'gest_rest.platos_quique',
          'menu',
          String ='Platos del menú'
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
          String ='Nombre del ingrediente',
          Required = True,
          help='Nombre del ingrediente utilizado en los platos'
     )

     description = fields.Text(
          String ='Descripcion del ingrediente',
          Required = True,
          help='Descripcion del ingrediente utilizado en los platos'
     )

     es_alergeno = fields.Boolean(
          String ='¿Es un alérgeno?',
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
     


