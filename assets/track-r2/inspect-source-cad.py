"""Read-only source-CAD audit. Requires installed cadquery/OCP. No geometry is repaired/exported.
Usage: python inspect-source-cad.py downloaded-RAIL_30_ASCE.igs
"""
from pathlib import Path
import argparse,hashlib,json
import cadquery as cq
from OCP.IGESControl import IGESControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.Interface import Interface_Static
parser=argparse.ArgumentParser();parser.add_argument('iges');parser.add_argument('--output');args=parser.parse_args()
p=Path(args.iges);r=IGESControl_Reader()
Interface_Static.SetCVal_s('xstep.cascade.unit','MM')
assert Interface_Static.CVal_s('xstep.cascade.unit')=='MM','Cannot confirm output millimetres'
assert r.ReadFile(str(p))==IFSelect_RetDone,'IGES read failed'
g=r.IGESModel().GlobalSection();r.TransferRoots();s=cq.Shape.cast(r.OneShape());b=s.BoundingBox();faces=cq.Compound.makeCompound(s.Faces());fb=faces.BoundingBox()
out=dict(issue='PF-3R2-R0',source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),source_IGES_unit_flag=g.UnitFlag(),source_IGES_unit_name=g.UnitName().ToCString(),import_system_unit='MM',loaded_roots=r.NbRootsForTransfer(),imported_faces=len(s.Faces()),imported_solids=len(s.Solids()),valid_shape=s.isValid(),all_shape_bbox_mm=dict(x_min=b.xmin,x_max=b.xmax,y_min=b.ymin,y_max=b.ymax,z_min=b.zmin,z_max=b.zmax),faces_bbox_size_mm=[fb.xlen,fb.ylen,fb.zlen],paper30ASCE_height_and_base_mm=[3.125*25.4,3.125*25.4],mismatch_mm=[fb.xlen-3.125*25.4,fb.ylen-3.125*25.4],accepted_profile=False,warning='Kernel validity does not establish correct component identity. Linked CAD conflicts with30ASCE paper envelope; no substitute family identified or scaling authorized.')
print(json.dumps(out,indent=2))
if args.output:Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
