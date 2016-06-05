#include <iostream>
#include <sstream>
using namespace std;

class prior
{
	public:
		prior() : type("none"), str_info("") {}
		void info() { cout << "prior : " << type << " ; " << str_info << endl; }
		double llh(double x) { return 0; }
		double chi2(double x) { return -2*llh(x); }

	// private data cannot be modified by subclasses, but "protected" can
	protected:
		string type;
		string str_info;
};

class uniform
	: public prior
{
	public:
		uniform(double offset) : offset(offset) {
			type = "uniform";
			str_info = "offset = " + to_string(offset);
		}
		double llh(double x) { return offset; }

	private:
		const double offset;
};

int main(void)
{
	prior p;
	p.info();
	cout << "p.llh(1) = " << p.llh(1) << endl;
	cout << "p.chi2(1) = " << p.chi2(1) << endl;
	cout << "p.llh(1) = " << p.llh(2) << endl;
	cout << "p.chi2(1) = " << p.chi2(2) << endl << endl;

	uniform u(-0.2);
	u.info();
	cout << "u.llh(1) = " << u.llh(1) << endl;
	cout << "u.chi2(1) = " << u.chi2(1) << endl << endl;
	cout << "u.llh(2) = " << u.llh(1) << endl;
	cout << "u.chi2(2) = " << u.chi2(1) << endl << endl;

	return 0;
};
