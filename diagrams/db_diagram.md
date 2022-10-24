```mermaid
erDiagram
	SubCriteria {
		uuid sub_criteria PK
		uuid criteria_id FK
	}
	Criteria {
		uuid criteria_id
		string criteria_name
		uuid round_id FK
		enum criteria_type  "Selects if the criteria is for compliance or scoring"
	}
	Assessors {
		uuid assessor_id FK "Uses account store id."
		uuid assessment_id FK
	}
	Assessments {
		uuid assessment_id PK
		enum status
		uuid application_id
		uuid round_id FK
		uuid fund_id
	}
	Sections {
		uuid sections_id PK	
		uuid sub_criteria_id FK		
		integer order
	}
	Fields {
		uuid field_id PK
		uuid sections_id FK
		string field_display_type "This is used to decide how the answers are displayed in the frontend."
		integer order
	}
	SectionsData {
		uuid sections_id FK
		string title
		enum langauge
	}
	FieldData {
		uuid field_id FK
		string title
		enum langauge		
	}
	Answers {
		uuid answer_id PK
		uuid field_id FK
		uuid assessment_id FK
		uuid application_id FK
		string answer
	}
	ScoresAndJustifications {
		uuid score_id PK
		uuid sub_criteria FK
		uuid assessment_id FK
		uuid assessor_id
		integer score
		string justification
		datetime submission_dt
	}
	AssessmentCompliance {
		uuid compliance_id PK
		uuid assessor_id FK
		uuid assessment_id FK
		boolean is_compliant
	}
	Comments {
		uuid comment_id PK
		uuid Sections_id FK
		uuid assessor_id FK
		uuid assessment_id FK
		string comment
		datetime created_at
	}

	Criteria ||--|{ SubCriteria : ""
	AssessmentCompliance ||--|| Criteria : ""
	SubCriteria ||--|{ Sections : ""
	Sections ||--|{ Fields : ""
	Sections ||--|{ SectionsData : ""
	Fields ||--|{ FieldData : ""
	Fields ||--|{ Answers : ""
	Assessments ||--|{ ScoresAndJustifications : ""
	ScoresAndJustifications ||--o| SubCriteria : ""
	Assessments }|--|{ Assessors : ""
	Assessments ||--|{ Criteria : ""
	Assessments ||--|{ Comments : ""
	Assessments ||--|{ AssessmentCompliance : ""
	Assessors ||--|{ Comments : ""
	Comments ||--|| Sections : ""
```
