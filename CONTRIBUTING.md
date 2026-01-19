# Contributing to Ripple Structure Simulation

Thank you for your interest in contributing to this project! This simulation is part of ongoing research into cooperation as information flow.

## Ways to Contribute

### 1. Report Issues
- Bug reports
- Documentation improvements
- Feature requests

### 2. Code Contributions
- Performance optimizations
- Additional metrics (e.g., betweenness centrality)
- New visualization options
- Support for additional data formats

### 3. Research Collaboration
For empirical validation using full YOROSIX datasets, contact:  
kazutaka.hayashi@yorosix.com

## Development Setup

```bash
# Clone repository
git clone https://github.com/kazutakahayashiyorosix/Ripple_Structures_and_Behavioral_Digital_Twins.git
cd Ripple_Structures_and_Behavioral_Digital_Twins

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests with sample data
python ripple_simulation.py sample_data/


Code Style
	∙	Follow PEP 8
	∙	Use descriptive variable names
	∙	Add docstrings to functions
	∙	Keep functions focused and testable
Pull Request Process
	1.	Fork the repository
	2.	Create a feature branch (git checkout -b feature/AmazingFeature)
	3.	Commit your changes (git commit -m 'Add AmazingFeature')
	4.	Push to the branch (git push origin feature/AmazingFeature)
	5.	Open a Pull Request
Research Ethics
This project studies naturally occurring cooperative behavior. When contributing:
	∙	Respect data privacy (all IDs must be anonymized)
	∙	Do not include personally identifiable information
	∙	Follow non-interventional observation principles
Questions?
Open an issue or contact: kazutaka.hayashi@yorosix.com
