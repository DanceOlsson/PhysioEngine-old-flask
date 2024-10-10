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
    }
}