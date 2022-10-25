```mermaid
erDiagram
	AssessorAssessment {
		uuid assessor_id FK "Uses account store id."
		uuid assessment_id FK
	}
	Assessments {
		uuid assessment_id PK
		enum status
		uuid application_id
		uuid round_id FK
		uuid fund_id
		enum langauge 
		boolean is_compliant  "Calculated from SectionCompliance"
	}
	AssessmentApplicationJson {
		uuid assessment_id FK
		json application_json
	}
	SubCriteriaScores {
		uuid score_id PK
		uuid sub_criteria  "File Lookup"
		uuid assessment_id FK
		uuid assessor_id
		integer score
		string justification
		datetime submission_dt
	}
	SectionCompliance {
		uuid sections_id FK "File Lookup"
		uuid assessor_id FK
		uuid assessment_id FK
		boolean is_compliant
	}
	SectionComments {
		uuid comment_id PK
		uuid sections_id FK "File Lookup"
		uuid assessor_id FK
		uuid assessment_id FK
		string comment
		datetime created_at
	}
	Metadata {
		uuid field_key
		uuid sub_criteria_id
		uuid criteria_id
		uuid section_id
		int order
		int section_order
		enum langauge
	}
		
	
	
	Assessments ||--|{ SubCriteriaScores : ""
	Assessments ||--|{ SectionComments : ""
	Assessments ||--|{ SectionCompliance : ""
	Assessments ||--|{ AssessmentApplicationJson : ""
	Assessments ||--|{ AssessorAssessment : ""
	AssessorsAD ||--|{ SectionComments : ""
	AssessorsAD ||--|{ SubCriteriaScores : ""
	AssessorsAD ||--|{ SectionCompliance : ""
	AssessorAssessment }|--|| AssessorsAD : ""
```
