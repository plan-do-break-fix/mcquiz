

## Terms

- Question - Consists of one or more Question Content objects and one or more Answer Forms
- Question Content - A generic object that may contain text, graphics, or other information to display to the user
- Answer Form - A field or interface component which provides zero or more Answer Choices and accepting one Answer Selection
- Answer Choice - An answer provided to the user which may or may not be correct
- Answer Selection - One or more answers submitted by a user in response to a Question
  - An Answer Selection consists of one or more Answers



## Creating a Quiz

The user input that generates the material used in quizzes is a yaml file that consists of Questions and Directives.

Question Fields:

- Question
- Correct
- Incorrect
- Image

Question - Principal unit of a quiz
         - Container for textual and graphical question content, one or more sets of correct answer, and zero or more sets of answer choices.

Basic Question Dictionary

- Question
- Correct

### Limiting Assumptions

- Question text does not repeat within a 

## Question Types

### **Provide** - aka Fill in the blank, short answer

- The question has no answer choices

Required Fields

- Question
- Correct

### **Choose** - aka Multiple choice, includes True/False

- The correct answer to the question is a selection of one or more displayed choices
- Answer choices are expected to be unique

Required Fields

- Question
- Correct
- Incorrect

Parameter Fields

- Shuffle - Randomize answer choice display order
- StrictOrder - require answer selection be given in same order as in **Correct**
- Image - string or list of strings - path to image(s) to be displayed



### TODO

- Ability to flag problem questions for admin review
- Graphic content support
- Sections - Allow multiple answer choice / answer selection lists for a single question
- Question Sets - Enables questions to appear in a predetermined order even when `shuffle == True`


## Data Records and Analysis

### Question Indexing

An Indexed Question has:

- A fingerprint recorded in the identity table
- Its n-grams recorded in the lexical directory table
- Its toString() output recorded in the question table

### Question Fingerprinting

#### Considerations

The syntactic flexibility of question definition results in a many-to-one mapping of question definitions to indexed questions. 

### Quiz Records