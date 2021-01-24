# Sizes and QR codes

**Assumption 1**:  post 2012 android/iOS cellphone in 'handheld' situation can display/scan around 1200 bytes of Qr code reliably.

**Assumption 2**: there is some minimal data set for a vaccination record.

**Assumption 3**: there may be some forms of private use that do require even less data

Inspiration here are some PL and CZ experiments - static QR on paper; and in the PL case - with just the citizens initials *but not the full name*.


##  Simple synthetic example from fHIR site

Resulting sizes:

Format 		         	| Size (Bytes)
------------------------|---------------------
Uncompressed JSON 		| 2698
xz compression 			| 876
Google protobuf v3.14.0 | 857
xz (opt: -e) / protobuf	| 596
CMS / PKI sig as ASN.1/DER	| ~400-600
CL signature			|~600-700

Conclusion: xz compress or protobuf alone will get you to the required size you need, with xz compress on protobuf giving you a further advantage - for this example down to around 600 bytes. And as this example is still overly large - this certainly allows for ZKP based (e.g. CL) signatures.


## Files 

* immunization.json 

	which is the example from the HL7 FHIR website stripped of the HTML displayable synopsis at the beginning but otherwise has
	kept the example values to give some kind of realistic feel

* immunization.proto 

     the google protocol buffer description of the JSON (there  seems to be an issue with marking field Performer as repeated so I left is as optional and it seems to work anyway)

* immunization_pb2.py 

 the protoc generated Python code

* immun.py 

	the Python script to create, populate and write out an immunization data structure in google protobuf format to a file

* gen-rsa.sh

  generate the CL and PKI signatures for size measuring.
  

