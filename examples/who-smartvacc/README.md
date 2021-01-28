# who-smartvacc

This experiment is to use a very specific selection of items to serialize to a protobuf.
The selection of items is guided by the *draft* version of the WHO requirements for a minimum data 
set for vaccination certificates.

Current work for defining a minimum data set focuses on medical use. There is already a standard
medical message for immunization in HL7 (both v3 CDA and FHIR) which can be re-used also for 
COVID-19 purposes. In fact, snomed and ICD-10 [^1] have simply extended their coding schemes in an 
"emergency" update to cater for COVID-19 specifics thus indicating that existing mechanisms 
for conveying immunization information are suitable also for re-use with COVID-19.

Given that a suitable HL7 message already exists for immunization and that the overhead for 
creating and maintaining a separate message is high, it seems appropriate to use that same 
message as the source for the subset of vaccination details required for a vaccination certificate.

The approach to generating the required binary data for placement e.g. in a QR code is to 
hand-code the .proto file to only extract those fields identified as the minimum data set for 
vaccination certificates from the larger overall message intended for more general purpose medical 
usage. This is data reduction at a semantic level first and foremost and typically often provides 
the most gain in terms of data reduction. In addition to this, we then transform this data into a 
more compact representation using the standard google protobuf packaging. We shrink this binary 
file still further by using compression (e.g xz) on the file. This is the final binary which can 
then be placed in e.g. a QR code (after possible encryption and then being digitally signed).

To get started, run build_pb.sh which in turn calls build_pb.py with some settings / args/


size | proto    | file 
-----|----------|-----------------------------
5953 | json     | Vaccination-FHIR-Bundle - GC.json
102  | protobuf | Vaccination-FHIR-Bundle - GC.bin
156  | xz(lmpa) |  Vaccination-FHIR-Bundle - GC.bin.xz


[^1]: ICD-11 will be release shortly containing these "emergency" codes as part of the core standard)
