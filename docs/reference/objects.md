
## BOMItem
`csfunctions.objects.BOMItem`

|Attribute|Type|Description|
|-|-|-|
|baugruppe|str \| None|Assembly|
|b_index|str \| None|Assembly Index|
|component_materialnr_erp|str \| None|Material Number ERP Component|
|netto_durchm|float \| None|Net. Diameter|
|netto_hoehe|float \| None|Net. Height|
|netto_laenge|float \| None|Net. Length|
|netto_breite|float \| None|Net. Width|
|position|int \| None|Position|
|menge|float \| None|Quantity|
|stlbemerkung|str \| None|Remarks|
|mengeneinheit|str \| None|Unit of Measure|

## Briefcase
`csfunctions.objects.Briefcase`

Briefcases are used by Workflows and can contain parts, documents or engineering changes.

|Attribute|Type|Description|
|-|-|-|
|cdb_object_id|str|Briefcase ID|
|name|str \| None|Briefcase Name|
|part_ids|list[str]|List of part IDs in this Briefcase. (teilenummer@t_index)|
|document_ids|list[str]|List of document IDs in this Briefcase. (z_nummer@z_index)|
|engineering_change_ids|list[str]|List of engineering change IDs in this Briefcase. (cdb_ec_id)|
|parts|list[[Part](objects.md#part)]||
|documents|list[[Document](objects.md#document)]||
|engineering_changes|list[[EngineeringChange](objects.md#engineeringchange)]||

## Document
`csfunctions.objects.Document`

Normal Document that doesn't contain a CAD-Model.

|Attribute|Type|Description|
|-|-|-|
|z_nummer|str|document number|
|z_index|str|index|
|titel|str \| None|title|
|category1_name_en|str \| None|Main Category|
|category1_name_de|str \| None|Main Category|
|category2_name_en|str \| None|Category|
|category2_name_de|str \| None|Category|
|z_categ1|str \| None|Main Category|
|z_categ2|str \| None|Category|
|cdb_obsolete|int|Obsolete|
|z_status|int|Status Number|
|z_status_txt|str|Status Text|
|autoren|str \| None|Authors, comma separated|
|z_bereich|str \| None|Department.|
|z_language|str \| None|language|
|keywords|str \| None|Keywords|
|z_bemerkung|str \| None|Remarks|
|joined_status_name|str \| None|Status|
|erzeug_system|str \| None|Program that created the document|
|cdb_lock|str \| None|User that locked the document.|
|mapped_cdb_lock_name|str \| None|Username that locked the document.|
|ce_valid_from|date \| datetime \| None|Effective from|
|ce_valid_to|date \| datetime \| None|Effective to|
|cdb_ec_id|str \| None|Engineering Change ID|
|ursprungs_z|str \| None|Origin|
|teilenummer|str \| None|Part No.|
|t_index|str \| None|Part Index|
|cdb_project_id|str \| None|Project No.|
|project_name|str \| None|Project Name|
|src_name|str \| None|Source|
|src_cdate|datetime \| None|Source created on|
|src_rdate|datetime \| None|Source received on|
|src_number|str \| None|Original No.|
|src_index|str \| None|Original Index|
|src_fname|str \| None|Original Filename|
|source_oid|str \| None|Based on Template|
|cdb_cpersno|str \| None|Created by|
|mapped_cdb_cpersno_name|str \| None|Created by|
|cdb_cdate|datetime \| None|Created on|
|cdb_mpersno|str \| None|Last Modified by|
|mapped_cdb_mpersno_name|str \| None|Last Modified by|
|cdb_mdate|datetime \| None|Last Modified on|
|cdb_m2persno|str \| None|File Last Saved by|
|mapped_cdb_m2persno_name|str \| None|File Last Saved by|
|cdb_m2date|datetime \| None|File Last Saved on|
|z_art|str \| None|Document Type|
|mapped_materialnr_erp|str \| None|Materialnumber ERP|
|files|list[[File](objects.md#file)]|Files attached to the document|
|part|typing.Optional[[Part](objects.md#part)]||

## EngineeringChange
`csfunctions.objects.EngineeringChange`

|Attribute|Type|Description|
|-|-|-|
|cdb_ec_id|str|Engineering Change ID|
|cdb_project_id|str \| None|Project ID|
|ec_state|str||
|end_time_plan|datetime \| None|Planned end time|
|status|int|Status|
|title|str \| None|Title|
|template_ec_id|str \| None|Template ID|
|c_department|str \| None|Department|
|c_description|str \| None|Description|
|c_event|str \| None|Event|
|c_reason|str \| None|Reason|
|c_source|str \| None|Source|
|category|str \| None|Category|
|part_ids|list[str]|List of part IDs, that were changed. (teilenummer@t_index)|
|document_ids|list[str]|List of document IDs, that were changed. (z_nummer@z_index)|
|planned_changes_part_ids|list[str]|List of part IDs, that were planned to be changed. (teilenummer@t_index)|
|planned_changes_document_ids|list[str]|List of document IDs, that were planned to be changed. (z_nummer@z_index)|
|accompanying_document_ids|list[str]|List of document IDs, that accompany the change. (z_nummer@z_index)|
|parts|list[[Part](objects.md#part)]||
|documents|list[[Document](objects.md#document)]||
|planned_changes_parts|list[[Part](objects.md#part)]||
|planned_changes_documents|list[[Document](objects.md#document)]||
|accompanying_documents|list[[Document](objects.md#document)]||
|cdb_cpersno|str \| None|Created by|
|cdb_cdate|datetime \| None|Created on|
|cdb_mpersno|str|Last Modified by|
|cdb_mdate|datetime \| None|Last Modified on|

## File
`csfunctions.objects.File`

|Attribute|Type|Description|
|-|-|-|
|cdb_object_id|str|ID|
|cdbf_name|str \| None|file name|
|cdbf_type|str \| None|file type|
|cdb_cpersno|str \| None|Created by|
|mapped_cdb_cpersno_name|str \| None|Created by|
|cdb_cdate|datetime \| None|Created on|
|cdb_mpersno|str \| None|Last Modified by|
|mapped_cdb_mpersno_name|str \| None|Last Modified by|
|cdb_mdate|datetime \| None|Last Modified on|
|blob_url|str \| None|Presigned Blob URL|

## Material
`csfunctions.objects.Material`

|Attribute|Type|Description|
|-|-|-|
|cdb_object_id|str \| None|Object ID|
|material_index|str \| None|Material Index|
|material_id|str \| None|Material ID|
|name_de|str \| None|Name DE|
|name_en|str \| None|Name EN|

## ObjectPropertyValue
`csfunctions.objects.ObjectPropertyValue`

An objects property, used by classification.

|Attribute|Type|Description|
|-|-|-|
|ref_object_id|str|Referenced Object|
|boolean_value|int \| None|Boolean Value|
|datetime_value|datetime \| None|Datetime Value|
|float_value|float \| None|Float Value|
|float_value_normalized|float \| None|Float Value Normalized|
|integer_value|int \| None|Integer Value|
|iso_language_code|str \| None|ISO Language Code|
|value_pos|int \| None|Position|
|property_code|str \| None|Property Code|
|property_path|str \| None|Property Path|
|property_type|str \| None|Property Type|
|range_identifier|str \| None|Range ID|
|text_value|str \| None|Text|

## Part
`csfunctions.objects.Part`

|Attribute|Type|Description|
|-|-|-|
|teilenummer|str|part number|
|t_index|str|part index|
|status|int|Status Number|
|materialnr_erp|str \| None|Material No. (ERP)|
|benennung|str \| None|Name|
|eng_benennung|str \| None|Name|
|benennung2|str \| None|Additional Name|
|t_kategorie_name_de|str \| None|Category Name|
|t_kategorie_name_en|str \| None|Category Name|
|cdb_t_project_id|str \| None|Project ID|
|t_bereich|str \| None|Department|
|cdb_t_ec_id|str \| None|Engineering Change ID|
|item_maturity|int \| None|Maturity Level|
|gebrauchsstand_name_de|str \| None|Usage Status|
|gebrauchsstand_name_en|str \| None|Usage Status|
|ce_valid_from|date \| datetime \| None|Effective from|
|ce_valid_to|date \| datetime \| None|Effective to|
|mengeneinheit_name_de|str \| None|Quantity Unit|
|mengeneinheit_name_en|str \| None|Quantity Unit|
|st_gewicht|typing.Optional[float]|Weight (kg)|
|material_object_id|str \| None|Material ID|
|surface_name_en|str \| None|Surface|
|surface_name_de|str \| None|Surface|
|techdaten|str \| None|Engineering Data|
|cssaas_mirrored_from|str \| None|Mirror Part ID|
|t_ersatz_fuer|str \| None|Replacement for|
|t_ersatz_durch|str \| None|Replaced by|
|din|str \| None|Norms|
|bemerkung|str \| None|Remarks|
|cdb_copy_of_item_id|str \| None|Copy of ID|
|type_object_id|str \| None|BOM Type ID|
|cdb_depends_on|str \| None|Derived from|
|site_object_id|str \| None|Plant|
|cssaas_frame_add_attr_1|str \| None|Additional Attribute 1|
|cssaas_frame_add_attr_2|str \| None|Additional Attribute 2|
|cssaas_frame_add_attr_3|str \| None|Additional Attribute 3|
|cssaas_frame_add_attr_4|str \| None|Additional Attribute 4|
|cssaas_frame_add_attr_5|str \| None|Additional Attribute 5|
|cdb_cpersno|str \| None|Created by|
|cdb_cpersno_name|str \| None|Created by|
|cdb_cdate|datetime \| None|Created on|
|cdb_mpersno|str \| None|Last Modified by|
|cdb_mpersno_name|str \| None|Last Modified by|
|cdb_mdate|datetime \| None|Last Modified on|
|cdb_m2persno|str \| None|File Last Saved by|
|cdb_m2persno_name|str \| None|File Last Saved by|
|cdb_m2date|datetime \| None|File Last Saved on|
|st_durchmesser|float \| None|Diameter|
|st_laenge|float \| None|Length|
|st_hoehe|float \| None|Height|
|cdb_object_id|str \| None|Object ID|
|site_erp|str \| None|Plant|
|fertart|str \| None|Production Type|
|t_pruef_datum|datetime \| None|Release Date|
|oberflaeche|str \| None|Surface|
|mengeneinheit|str \| None|Unit of Measure|
|gebrauchsstand|str \| None|Usability|
|st_breite|float \| None|Width|
|document_ids|list[str]|List of document IDs, that were changed. (z_nummer@z_index)|
|documents|list['Document']||

## Workflow
`csfunctions.objects.Workflow`

|Attribute|Type|Description|
|-|-|-|
|cdb_process_id|str|Workflow ID|
|title|str \| None|Title|
|started_at|datetime \| None|Date when the workflow was started.|
|started_by|str \| None|ID of the user who started the workflow.|
|local_briefcase_ids|list[str]|List of local briefcase ids (cdb_object_id)|
|global_briefcase_ids|list[str]|List of global briefcase ids (cdb_object_id)|
|local_briefcases|list[[Briefcase](objects.md#briefcase)]||
|global_briefcases|list[[Briefcase](objects.md#briefcase)]||
