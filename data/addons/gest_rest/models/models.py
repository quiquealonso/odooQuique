from odoo import models, fields


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
     tiempo_preparacion = fields.Integer(
          String ='Tiempo de preparación del plato',
          Required = True,
          help='Tiempo que tarda el plato en ser cocinado'
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
     


