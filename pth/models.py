from django.db import models

# Create your models here.
class Bu(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "tbl_bu"


class Line(models.Model):
    name = models.CharField(max_length=255)
    preheat_method = models.CharField(max_length=255, null=True)
    solder_type = models.CharField(max_length=255, null=True)
    ping_time = models.DateTimeField(null=True)
    status = models.BooleanField(null=True)
    sfis_name = models.CharField(max_length=15,null=True)
    bu = models.ForeignKey(
        'Bu',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "tbl_line"


class Model(models.Model):
    name = models.CharField(max_length=255, null=True)
    thinkness = models.CharField(max_length=255, null=True)
    surface_type = models.CharField(max_length=255, null=True)
    image_url = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "tbl_model"


class Params(models.Model):

    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    machine_type = models.ForeignKey('MachineType', on_delete=models.CASCADE)
    class Meta:
        db_table = "tbl_params"


class Params_data(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.FloatField(null=True)

    time = models.DateTimeField(null=True)
    line = models.ForeignKey(
        'Line',
        on_delete=models.CASCADE
    )
    params = models.ForeignKey(
        'Params',
        on_delete=models.CASCADE
    )
    setting = models.ForeignKey(
        'Params_settings',
        on_delete=models.CASCADE,
        null=True
    )
    class Meta:
        db_table = "tbl_params_data"
class Params_settings(models.Model):
    class Meta:
        db_table = "tbl_params_setting"
    id = models.BigAutoField(primary_key=True)
    value = models.FloatField(null=True)
    time = models.DateTimeField(null=True)
    line = models.ForeignKey(
        'Line',
        on_delete=models.CASCADE
    )
    params = models.ForeignKey(
        'Params',
        on_delete=models.CASCADE
    )


class Line_Model(models.Model):
    line = models.ForeignKey(
        'Line',
        on_delete=models.CASCADE
    )
    model = models.ForeignKey(
        'Model',
        on_delete=models.CASCADE
    )
    url = models.FileField(upload_to= 'images',null=True)

    class Meta:
        db_table = "tbl_line_model"


class Spec(models.Model):
    lsl = models.CharField(max_length=255)
    usl = models.CharField(max_length=255)

    params = models.ForeignKey(
        'Params',
        on_delete=models.CASCADE
    )
    line_model = models.ForeignKey(
        'Line_Model',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "tbl_spec"


class Material(models.Model):
    datasheet_url = models.CharField(max_length=255, null=True)
    spec_img_url = models.CharField(max_length=255, null=True)
    dimension_url1 = models.CharField(max_length=255, null=True)
    dimension_url2 = models.CharField(max_length=255, null=True)
    dimension_url3 = models.CharField(max_length=255, null=True)
    schematic_img_url = models.CharField(max_length=255, null=True)
    material_number = models.CharField(max_length=255, null=True)
    dataset_url = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "tbl_material"


class Component(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    image_url = models.CharField(max_length=255, null=True)
    spec_url = models.CharField(max_length=255, null=True)
    direction = models.CharField(max_length=255, null=True)
    layout = models.CharField(max_length=255, null=True)
    material_number = models.CharField(max_length=255, null=True)
    distance_to_nearest_component = models.DecimalField(
        max_digits=20, decimal_places=2, null=True)
    image_on_sop_url = models.CharField(max_length=255, null=True)
    model = models.ForeignKey(
        'Model',
        on_delete=models.CASCADE
    )
    materials = models.ManyToManyField(Material)

    class Meta:
        db_table = "tbl_component"


class Pin_infor(models.Model):
    length = models.IntegerField(null=True)
    dimension = models.CharField(max_length=255, null=True)
    index = models.IntegerField(null=True)
    material = models.ForeignKey(
        'Material',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "tbl_pin_infor"


class Solder_Point_Specification(models.Model):
    component = models.ForeignKey(
        'Component',
        on_delete=models.CASCADE
    )
    hole_shape = models.CharField(max_length=255, null=True)
    pad_shape = models.CharField(max_length=255, null=True)
    hole_size = models.CharField(max_length=255, null=True)
    pad_size = models.CharField(max_length=255, null=True)
    index = models.IntegerField(null=True)

    class Meta:
        db_table = "tbl_solder_point_specification"


class Inspection_image(models.Model):
    url = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "tbl_inspection_image"
class Carrier_result(models.Model):
    id = models.BigAutoField(primary_key=True)
    carrier_number = models.CharField(max_length=255, null=True)
    time = models.DateTimeField(null=True)
    class Meta:
        db_table = "tbl_carrier_result"

class PCB_result(models.Model):
    id = models.BigAutoField(primary_key=True)
    sn = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=5, null=True)
    carrier_number = models.CharField(max_length=25, null=True)
    pcb_index = models.IntegerField(null=True)
    material_number = models.CharField(max_length=25,null=True)
    date_code = models.CharField(max_length=15, null=True)
    pcb_desc = models.CharField(max_length=100, null=True)
    lot_code = models.CharField(max_length=15,null=True)
    time = models.DateTimeField(null=True)
    line = models.CharField(max_length=255, null=True)
    smt_to_pth = models.IntegerField(null=True)
    insp2_to_pth = models.IntegerField(null=True)
    indexes = [
        models.Index(fields=['material_number',]),
        models.Index(fields=['pcb_desc',]),
        models.Index(fields=['date_code',]),
        models.Index(fields=['lot_code',])
    ]
    line_model = models.ForeignKey(
        'Line_Model',
        on_delete=models.CASCADE
    )
    carrier_result = models.ForeignKey(
            'Carrier_result',
            on_delete=models.CASCADE,null=True
        )
    class Meta:
        db_table = "tbl_pcb_result"





class Component_Result(models.Model):
    id = models.BigAutoField(primary_key=True)
    time = models.DateTimeField(null=True)
    date_code = models.CharField(max_length=10, null=True)
    material_number = models.CharField(max_length=25, null=True)
    lot_code = models.CharField(max_length=10, null=True)
    roi_x = models.IntegerField(null=True)
    roi_y = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    component = models.ForeignKey(
        'Component',
        on_delete=models.CASCADE
    )
    pcb_result = models.ForeignKey(
        'PCB_result',
        on_delete=models.CASCADE
    )
    inspection_image = models.ForeignKey(
        'Inspection_image',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "tbl_component_result"


class PCB_component_pin(models.Model):
    id = models.BigAutoField(primary_key=True)
    index = models.IntegerField(null=True)
    status = models.CharField(max_length=5, null=True)
    time = models.DateTimeField(null=True)
    error_code = models.CharField(max_length=25, null=True)
    roi_x = models.IntegerField(null=True)
    roi_y = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    angle = models.FloatField(null=True)
    line = models.CharField(max_length=255, null=True)
    model = models.CharField(max_length=255, null=True)
    component_result = models.ForeignKey(
        'Component_Result',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "tbl_pcb_component_pin"


class Params_Of_PCB(models.Model):
    id = models.BigAutoField(primary_key=True)
    min = models.FloatField(null=True)
    max = models.FloatField(null=True)
    pcb_result = models.ForeignKey(
        'PCB_result',
        on_delete=models.CASCADE
    )
    param = models.ForeignKey(
        'Params',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "tbl_params_of_pcb"

class Params_Detail_Of_PCB(models.Model):
    id = models.BigAutoField(primary_key=True)
    param_data =  models.ForeignKey(
        'Params_data',
        on_delete=models.CASCADE
    )
    pcb_result = models.ForeignKey(
        'PCB_result',
        on_delete=models.CASCADE
    )
    param = models.ForeignKey(
        'Params',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "tbl_params_detail_of_pcb"





class Carrier_Code(models.Model):
    model_name = models.CharField(max_length=255)
    bu = models.ForeignKey(
        'Bu',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "tbl_carrier_code"
    
class MachineType(models.Model):
    machine_type = models.CharField(max_length=255,null=True)
    class Meta:
        db_table = "tbl_machine_type"
