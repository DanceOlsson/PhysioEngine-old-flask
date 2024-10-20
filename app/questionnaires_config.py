QUESTIONNAIRES = {
    'koos': {
        'name': 'KOOS (Knee injury and Osteoarthritis Outcome Score)',
        'sections': {
            'Pain': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9'],
            'Symptoms': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7'],
            'ADL': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17'],
            'Sport/Rec': ['SP1', 'SP2', 'SP3', 'SP4', 'SP5'],
            'QOL': ['Q1', 'Q2', 'Q3', 'Q4']
        },
        'score_range': (0, 100),
        'interpretation': {
            (0, 25): 'Severe problems',
            (26, 50): 'Moderate problems',
            (51, 75): 'Mild problems',
            (76, 100): 'No significant problems'
        }
    },
    'hoos': {
        'name': 'HOOS (Hip dysfunction and Osteoarthritis Outcome Score)',
        'sections': {
            'Symptoms': ['S1', 'S2', 'S3', 'S4', 'S5'],
            'Pain': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10'],
            'ADL': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17'],
            'Sport/Rec': ['SP1', 'SP2', 'SP3', 'SP4'],
            'QOL': ['Q1', 'Q2', 'Q3', 'Q4']
        },
        'score_range': (0, 100),
        'interpretation': {
            (0, 25): 'Severe problems',
            (26, 50): 'Moderate problems',
            (51, 75): 'Mild problems',
            (76, 100): 'No significant problems'
        }
    },
    'dash_swedish': {
        'name': 'DASH (Disabilities of the Arm, Shoulder and Hand) - Svenska',
        'sections': {
            'Förmåga att utföra aktiviteter': ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17', 'Q18', 'Q19', 'Q20', 'Q21'],
            'Påverkan på socialt liv och dagliga aktiviteter': ['Q22', 'Q23'],
            'Symtom': ['Q24', 'Q25', 'Q26', 'Q27', 'Q28'],
            'Sömn och självförtroende': ['Q29', 'Q30'],
            'Arbetsförmåga': ['Q31', 'Q32', 'Q33', 'Q34', 'Q35', 'Q36'],
            'Musik och idrott': ['Q37', 'Q38', 'Q39', 'Q40', 'Q41', 'Q42']
        },
        'score_range': (0, 100),
        'interpretation': {
            (0, 25): 'Minimal funktionsnedsättning',
            (26, 50): 'Mild funktionsnedsättning',
            (51, 75): 'Måttlig funktionsnedsättning',
            (76, 100): 'Allvarlig funktionsnedsättning'
        },
        'file': 'dash_swedish.json',
        'template': 'dash_swedish.html',
        'language': 'sv'
    }
}