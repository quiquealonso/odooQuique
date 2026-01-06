from odoo import models, fields, api


class platos_quique(models.Model):
     _name = 'gest_rest.platos_quique'
     _description = 'gest_rest.platos_quique'

     codigo = fields.Char(
        compute="_get_codigo",
        string="Codigo"
     )

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
     precio_con_iva = fields.Float(
        compute="_compute_precio_con_iva",
        string="Precio con IVA"
     )
     tiempo_preparacion = fields.Integer(
          String ='Tiempo de preparación del plato',
          Required = True,
          help='Tiempo que tarda el plato en ser cocinado'
     )
     descuento = fields.Float(
          String ='Descuento (%)',
     )
     precio_final = fields.Float(
          String ='Precio final del plato',
          store = True,
          compute = 'compute_precio_final',
     )
     disponible = fields.Boolean(default=True)
     categoria = fields.Selection(
     [('entrada', 'Entrada'),
      ('plato_principal', 'Plato Principal'),
      ('postre', 'Postre'),
      ('bebida', 'Bebida')],
     string='Categoría', 
     required=True,
     help='Categoría del plato en el menú del restaurante')

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

     def _get_codigo(self):
        for plato in self:
            # Si el plato no tiene un menu asignado
            if not plato.menu:
                plato.codigo = "TSK_" + str(plato.id)
            else:
             # Si tiene menu, usamos su nombre
                plato.codigo = plato.categoria[:3].upper().upper() + "_" + str(plato.id)
     
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
     activo = fields.Boolean(default=True)
     platos = fields.One2many(
          'gest_rest.platos_quique',
          'menu',
          String ='Platos del menú'
     )
     precio_total = fields.Float(
               string='Precio total',
               store=True,
               compute='_compute_precio_total',
          )

     @api.depends('platos', 'platos.precio_final')
     def _compute_precio_total(self):
           for menu in self:
                precios = menu.platos.mapped('precio_final')
                menu.precio_total = sum(precios)
                
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
     platos = fields.Many2many(
          comodel_name='gest_rest.platos_quique',
          relation='Relacion_ingrediente_plato',
          column1='ingrediente_id',
          column2='plato_id',
          string='Platos que contienen este ingrediente'
     )
     


