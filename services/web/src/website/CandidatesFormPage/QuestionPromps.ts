import { Question } from '@/website/CandidatesFormPage/CandidatesForm/constants.ts';

export const questionPrompts: Question[] = [
    {
        prompt: 'What is your name?',
        question_type: 'GENERAL',
        answer_type: 'TEXT',
    },
    {
        prompt: 'What is your email?',
        question_type: 'GENERAL',
        answer_type: 'TEXT',
    },
    {
        prompt: 'What is your standing?',
        options: ['Freshman', 'Sophomore', 'Junior', 'Senior'],
        question_type: 'GENERAL',
        answer_type: 'MULTIPLE_CHOICE',
    },
    {
        prompt: 'What are your intended majors?',
        question_type: 'GENERAL',
        answer_type: 'TEXT',
    },
    {
        prompt: 'Are you currently part of any club?',
        options: ['Yes', 'No'],
        question_type: 'GENERAL',
        answer_type: 'SINGLE_CHOICE',
    },
    {
        prompt: 'How did you hear about The Hub?',
        question_type: 'GENERAL',
        answer_type: 'TEXT',
    },
    {
        prompt: 'Why do you want to join The Hub? What do you hope to take away from the club?',
        question_type: 'GENERAL',
        answer_type: 'TEXT',
    },
    {
        prompt: 'List 3 adjectives that describe you best.',
        question_type: 'GENERAL',
        answer_type: 'TEXT',
    },
    {
        prompt: 'Describe a situation where you had to work on a team. How did you handle differing opinions or approaches to solving a problem?',
        question_type: 'GENERAL',
        answer_type: 'TEXT',
    },
    {
        prompt: 'What is something about you we would never guess from this application?',
        question_type: 'PR',
        answer_type: 'TEXT',
    },
    {
        prompt: 'What is something people usually remember about you after meeting you?',
        question_type: 'PR',
        answer_type: 'TEXT',
    },
    {
        prompt: 'What is a random thing you are surprisingly good at?',
        question_type: 'PR',
        answer_type: 'TEXT',
    },
    {
        prompt: 'What is a rule you secretly enjoy breaking?',
        question_type: 'PR',
        answer_type: 'TEXT',
    },
    {
        prompt: 'What is your go-to way of breaking an awkward silence?',
        question_type: 'PR',
        answer_type: 'TEXT',
    },
    {
        prompt: 'What is one question you love asking people when you’re getting to know them?',
        question_type: 'PR',
        answer_type: 'TEXT',
    },
    {
        prompt: 'You have to organize a dinner for any 3 people in the world. Who is at the table? Why?',
        question_type: 'PR',
        answer_type: 'TEXT',
    },
    {
        prompt: 'If your life had a PR campaign right now, what would the slogan be?',
        question_type: 'PR',
        answer_type: 'TEXT',
    },
    {
        prompt: 'If you had to describe your personality using only three brands, which ones would you choose?',
        question_type: 'PR',
        answer_type: 'TEXT',
    },
    {
        prompt: 'If we gave you €50 and told you to make an ordinary Tuesday memorable for 10 people, what would you do?',
        question_type: 'PR',
        answer_type: 'TEXT',
    },
    {
        prompt: 'Call someone from The Hub and find out the ONE thing they would take with them if they had to leave for a spontaneous trip tomorrow. Write it below.',
        question_type: 'PR',
        answer_type: 'TEXT',
    },
    {
        prompt: 'Let’s say you have one month for a given project/homework, which will take you around 1 week. When will you initially start thinking about it? Be honest',
        question_type: 'DESIGN',
        answer_type: 'SINGLE_CHOICE',
        options: [
            'A couple of days after getting the homework/task',
            'After the first week has passed',
            'Exactly in the middle - after 2 weeks have passed',
            'In the final week before the deadline',
            'Last days before the deadline.',
        ],
    },
    {
        prompt: 'For the same project/homework. When will you actually start doing it?',
        question_type: 'DESIGN',
        answer_type: 'SINGLE_CHOICE',
        options: [
            'In a couple of days after getting the homework/task',
            'After the first week has passed',
            'Exactly in the middle - after 2 weeks have passed',
            'In the final week before the deadline',
            'Last days before the deadline.',
        ],
    },
    {
        prompt: 'For the same project/homework. About when do you plan to finish it realistically?',
        question_type: 'DESIGN',
        answer_type: 'SINGLE_CHOICE',
        options: [
            'In a couple of days after getting the homework/task',
            'After the first week has passed',
            'Exactly in the middle - after 2 weeks have passed',
            'In the final week before the deadline',
            'Last days before the deadline.',
        ],
    },
    {
        prompt: 'Are you familiar with some of the designing tools?',
        question_type: 'DESIGN',
        answer_type: 'MULTIPLE_CHOICE',
        options: [
            'Canva',
            'Figma (UI/UX & Web Design)',
            'Adobe Photoshop',
            'Adobe Illustrator',
            'Procreate / Digital Illustration',
            'Other',
            'I am not familiar with these yet, but I learn fast and want to start now!',
        ],
    },
    {
        prompt: 'Are there any tools that you have used?',
        question_type: 'DESIGN',
        answer_type: 'MULTIPLE_CHOICE',
        options: [
            'Canva',
            'Figma (UI/UX & Web Design)',
            'Adobe Photoshop',
            'Adobe Illustrator',
            'Procreate / Digital Illustration',
            'Other',
            'I am not familiar with these yet, but I learn fast and want to start now!',
        ],
    },
    {
        prompt: 'Are there any tools that you have used?',
        question_type: 'DESIGN',
        answer_type: 'TEXT',
    },
    {
        prompt:
            'Drop a link to anything visual you have made\n' +
            '(Note: A formal portfolio is ABSOLUTELY NOT required! School presentations, Canva posts, photography, sketches, or passion projects are more than welcome. )\n' +
            'If none, feel free to send something inspirational as design you found from pinterest/dribble/etc. If you share external designs, please clearly mention they are for inspiration, not made by you.',
        question_type: 'DESIGN',
        answer_type: 'TEXT',
    },
    {
        prompt: 'What is the first thing you think of when you hear the word “marketing”?',
        question_type: 'MARKETING',
        answer_type: 'TEXT',
    },
    {
        prompt: 'Imagine we have an event that nobody knows about. How would you get students interested in it?',
        question_type: 'MARKETING',
        answer_type: 'TEXT',
    },
    {
        prompt:
            'Have you ever used social media, advertising platforms, or video editing tools for a project, promotion, or work? If yes, which platforms or tools have you used?\n' +
            '* This is not a requirement, we’re just asking to get to know your experience and skills better.',
        question_type: 'MARKETING',
        answer_type: 'TEXT',
    },
    {
        prompt: 'If two brands sell similar products, how would you make their marketing campaigns different from each other?',
        question_type: 'MARKETING',
        answer_type: 'TEXT',
    },
    {
        prompt: 'If your life had a marketing campaign, what would the campaign be called?',
        question_type: 'MARKETING',
        answer_type: 'TEXT',
    },
    {
        prompt: 'An event starts in 20 minutes and you realize you’re missing something important. What do you do first?',
        question_type: 'LOGISTICS',
        answer_type: 'TEXT',
    },
    {
        prompt: 'The person bringing the equipment texts you: ‘I’m going to be 30 minutes late.’ What’s your move?',
        question_type: 'LOGISTICS',
        answer_type: 'TEXT',
    },
    {
        prompt: 'You’re organizing an event and suddenly three volunteers cancel. How do you handle it?',
        question_type: 'LOGISTICS',
        answer_type: 'TEXT',
    },
    {
        prompt: 'You’re given a task but the instructions are unclear and the person who assigned it is unavailable. What do you do?',
        question_type: 'LOGISTICS',
        answer_type: 'TEXT',
    },
    {
        prompt: 'Two people are responsible for the same task, and another task has no one assigned. What do you do?',
        question_type: 'LOGISTICS',
        answer_type: 'TEXT',
    },
    {
        prompt: 'What are the first 3 things you would do when you arrive at an event venue?',
        question_type: 'LOGISTICS',
        answer_type: 'TEXT',
    },
    {
        prompt: 'What’s more important: finishing everything or making sure the most important things are done correctly? Why?',
        question_type: 'LOGISTICS',
        answer_type: 'TEXT',
    },
    {
        prompt: 'What’s one thing that can ruin an event even if everything else is perfectly organized?',
        question_type: 'LOGISTICS',
        answer_type: 'TEXT',
    },
    {
        prompt: 'If logistics were a person at a party, what personality would they have?',
        question_type: 'LOGISTICS',
        answer_type: 'TEXT',
    },
    {
        prompt: 'Do you have any previous experience in programming? If yes, please provide further details (e.g. courses, bootcamps, internships, etc.)',
        question_type: 'DEVELOPMENT',
        answer_type: 'TEXT',
    },
    {
        prompt: 'What languages/technologies have you previously used?',
        question_type: 'DEVELOPMENT',
        answer_type: 'TEXT',
    },
    {
        prompt: 'If you can, please provide a link to your portfolio (e.g. GitHub, GitLab, Google Drive)',
        question_type: 'DEVELOPMENT',
        answer_type: 'TEXT',
    },
    {
        prompt: 'Can you give us any examples of problems you have solved/tried to solve while working on projects?',
        question_type: 'DEVELOPMENT',
        answer_type: 'TEXT',
    },
    {
        prompt: 'What is the dumbest way you have fixed a problem in your code?',
        question_type: 'DEVELOPMENT',
        answer_type: 'TEXT',
    },
    {
        prompt: 'What is the next technology you would like to learn?',
        question_type: 'DEVELOPMENT',
        answer_type: 'TEXT',
    },
    {
        prompt: 'Give at least two fields in computer science or IT that you would like to know more about?',
        question_type: 'DEVELOPMENT',
        answer_type: 'TEXT',
    },
    {
        prompt: 'Your project crashes 30 minutes before you have to present it in front of a potential client/investor. What do you do?',
        question_type: 'DEVELOPMENT',
        answer_type: 'TEXT',
    },
];
