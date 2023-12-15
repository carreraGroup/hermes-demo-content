library BCSE version '1.0.0'

using FHIR version '4.0.1'

include FHIRHelpers version '4.0.1' called FHIRHelpers

valueset "Absence of Left Breast": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1329'
valueset "Absence of Right Breast": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1330'
valueset "Bilateral Mastectomy": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1042'
valueset "Bilateral Modifier": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1043'
valueset "Clinical Bilateral Modifier": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1951'
valueset "Clinical Left Modifier": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1949'
valueset "Clinical Right Modifier": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1950'
valueset "Clinical Unilateral Mastectomy": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1948'
valueset "History of Bilateral Mastectomy": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1331'
valueset "Left Modifier": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1148'
valueset "Mammography": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1168'
valueset "Right Modifier": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1230'
valueset "Unilateral Mastectomy": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1256'
valueset "Unilateral Mastectomy Left": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1334'
valueset "Unilateral Mastectomy Right": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1335'

//pallative care
valueset "Palliative Care Assessment": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.2225'
valueset "Palliative Care Encounter": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1450'
valueset "Palliative Care Intervention": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.2224'

//Adv illness
valueset "Dementia Medications": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1729'
valueset "Frailty Device": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1530'
valueset "Frailty Diagnosis": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1531'
valueset "Frailty Encounter": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1532'
valueset "Frailty Symptom": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1533'

//Hospice
valueset "Hospice Encounter":'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1761'
valueset "Hospice Intervention": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1762'

valueset "Unused": 'https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1762'


parameter "Measurement Period Start" DateTime
parameter "Measurement Period End" DateTime

context Unfiltered

define function "Prevalence Period"(condition Condition) returns Interval<DateTime>:
  Interval[start of condition.onset, end of condition.abatement]

define "Initial Population":
    [Patient] p where p.gender = 'female' return p.id

define "Member Coverage":
  [Coverage] C
    where  C.period overlaps "Participation Period" and C.policyHolder.reference in "Initial Population"

define "Participation Period":
  Interval["Measurement Period Start", "Measurement Period End"]

define "Denominator":
  "Initial Population"

define "Hospice Intervention or Encounter":
([Procedure:"Hospice Intervention"] HospiceInt
    where HospiceInt.performed overlaps "Participation Period" and HospiceInt.status = 'completed'
    return HospiceInt.subject.reference)
union
([Encounter: "Hospice Encounter"] HospiceEnc
    where HospiceEnc.period overlaps "Participation Period" and HospiceEnc.status = 'finished'
    return HospiceEnc.subject.reference)

define "Exclusions":
  "Hospice Intervention or Encounter"
  union "Mastectomy Exclusion"
  union "Advanced Illness and Frailty Exclusion Not Including Over Age 80"
  union "Palliative Care Overlapping Period" ( "Participation Period" )

define "Mastectomy Exclusion":
//we should see if we can try to or these...
  (("Left Mastectomy Diagnosis" union "Right Mastectomy Diagnosis" union "Bilateral Mastectomy Diagnosis") C
    return C.subject.reference)
  union
  (("Left Mastectomy Procedure" union "Right Mastectomy Procedure" union "Bilateral Mastectomy Procedure") P
    return P.subject.reference)
  
define "Right Mastectomy Diagnosis":
  [Condition: "Absence of Right Breast"] RightMastectomyDiagnosis
    where RightMastectomyDiagnosis.onset.end >= "Measurement Period End" and RightMastectomyDiagnosis.clinicalStatus.coding.code = 'active'

define "Right Mastectomy Procedure":
  (( [Procedure: "Unilateral Mastectomy Right"] P where P.status = 'completed' )
    union ( [Procedure: "Unilateral Mastectomy"] UnilateralMastectomyProcedure
        where UnilateralMastectomyProcedure.bodySite.coding.code in "Right Modifier" and UnilateralMastectomyProcedure.status = 'completed'
    )
    union ( [Procedure: "Clinical Unilateral Mastectomy"] ClinicalUnilateralMastectomyProcedure
        where ClinicalUnilateralMastectomyProcedure.bodySite.coding.code in "Clinical Right Modifier" and ClinicalUnilateralMastectomyProcedure.status = 'completed'
    ) )
     RightMastectomyProcedure
    where RightMastectomyProcedure.performed.start <= "Measurement Period End"

define "Left Mastectomy Diagnosis":
  [Condition: "Absence of Left Breast"] LeftMastectomyDiagnosis
    where LeftMastectomyDiagnosis.onset.end >= "Measurement Period End" 
    and LeftMastectomyDiagnosis.clinicalStatus.coding.code = 'active'

define "Left Mastectomy Procedure":
  (( [Procedure: "Unilateral Mastectomy Left"] P where P.status = 'completed') 
    union ( [Procedure: "Unilateral Mastectomy"] UnilateralMastectomyProcedure
        where UnilateralMastectomyProcedure.bodySite.coding.code in "Left Modifier" and UnilateralMastectomyProcedure.status = 'completed'
    )
    union ( [Procedure: "Clinical Unilateral Mastectomy"] ClinicalUnilateralMastectomyProcedure
        where ClinicalUnilateralMastectomyProcedure.bodySite.coding.code in "Clinical Left Modifier" and ClinicalUnilateralMastectomyProcedure.status = 'completed'
    ) 
    ) LeftMastectomyProcedure
    //if we leave "start" off the end, the compiler should catch this
    where LeftMastectomyProcedure.performed.start <= "Measurement Period End"

define "Bilateral Mastectomy Diagnosis":
  [Condition: "History of Bilateral Mastectomy"] BilateralMastectomyHistory
    where BilateralMastectomyHistory.onset.start <= "Measurement Period End" 
    and BilateralMastectomyHistory.clinicalStatus.coding.code = 'active'

define "Bilateral Mastectomy Procedure":
  ((  [Procedure: "Bilateral Mastectomy"] )
    union ( [Procedure: "Unilateral Mastectomy"] UnilateralMastectomyProcedure
        where UnilateralMastectomyProcedure.bodySite.coding.code in "Bilateral Modifier" and UnilateralMastectomyProcedure.status = 'completed'
    )
    union ([Procedure: "Clinical Unilateral Mastectomy"] ClinicalUnilateralMastectomyProcedure
        where ClinicalUnilateralMastectomyProcedure.bodySite.coding.code in "Clinical Bilateral Modifier" and ClinicalUnilateralMastectomyProcedure.status = 'completed'
    ) ) BilateralMastectomyPerformed
    where BilateralMastectomyPerformed.performed.start <= "Measurement Period End"

define "Numerator":
   [Observation: "Mammography"] Mammogram
      where Mammogram.effective ends during "Participation Period"
      and Mammogram.subject.reference in "Initial Population"
  


//Advanced illness    

define "Advanced Illness and Frailty Exclusion Not Including Over Age 80":
  "Has Criteria Indicating Frailty"
  union 
  "Dementia Medications In Year Before or During Measurement Period"
    

define "Has Criteria Indicating Frailty":
  ( [Observation: "Frailty Device"] FrailtyDeviceApplied
      where FrailtyDeviceApplied.effective overlaps "Participation Period"
      return FrailtyDeviceApplied.subject.reference
  )
  union ( [Condition: "Frailty Diagnosis"] FrailtyDiagnosis 
      where FrailtyDiagnosis.clinicalStatus.coding.code = 'active' and "Prevalence Period" ( FrailtyDiagnosis ) overlaps "Participation Period"
      return FrailtyDiagnosis.subject.reference
  )
  union ( [Encounter: "Frailty Encounter"] FrailtyEncounter
      where FrailtyEncounter.period overlaps "Participation Period" and FrailtyEncounter.status = 'finished'
      return FrailtyEncounter.subject.reference
  )
  union ( [Observation: "Frailty Symptom"] FrailtySymptom
      where FrailtySymptom.effective overlaps "Participation Period"
      return FrailtySymptom.subject.reference
  )

define "Dementia Medications In Year Before or During Measurement Period":
  [MedicationDispense: "Dementia Medications"] DementiaMedDispensed
    where DementiaMedDispensed.status = 'completed'
    return DementiaMedDispensed.subject.reference
  


//Pallative care

define function "Palliative Care Overlapping Period"(Period Interval<DateTime>):
  ( [Observation: "Palliative Care Assessment"] PalliativeAssessment
      where PalliativeAssessment.effective overlaps Interval[date from start of Period, date from end of Period]
      return PalliativeAssessment.subject.reference
  )
  union ( [Encounter: "Palliative Care Encounter"] PalliativeEncounter
      where PalliativeEncounter.period overlaps Period and PalliativeEncounter.status = 'finished'
      return PalliativeEncounter.subject.reference
  )
  union ([Procedure: "Palliative Care Intervention"] PalliativeIntervention
      where PalliativeIntervention.performed overlaps Period and PalliativeIntervention.status = 'completed'
      return PalliativeIntervention.subject.reference
  )