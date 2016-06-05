#include <iostream>
#include <sstream>
using namespace std;

/*
 * Move towards more of a generic 'prior' object by including 'type' and
 * 'str_info' in constructor args
 *
 */

class prior
{
	public:
		prior(const string &type="none", const string &str_info="") : type(type), str_info(str_info) {}
		void info() { cout << "prior : " << type << " ; " << str_info << endl; }
		virtual double llh(double x) { return 0; }
		double chi2(double x) { return -2*llh(x); }

	private:
		const string type;
		const string str_info;
};

class uniform
	// inherit from "prior"
	: public prior
{
	public:
		// constructor for uniform...
		uniform(double offset) : offset(offset),
			// ... and initialize superclass using the new args
			prior("uniform", "offset = " + to_string(offset)) {}
		virtual double llh(double x) { return offset; }

	private:
		const double offset;
};

int main(void)
{
	prior p;
	p.info();
	cout << "p.llh(1) = " << p.llh(1) << endl;
	cout << "p.chi2(1) = " << p.chi2(1) << endl << endl;

	uniform u(-0.2);
	u.info();
	cout << "u.llh(1) = " << u.llh(1) << endl;
	cout << "u.chi2(1) = " << u.chi2(1) << endl << endl;

	return 0;
};
