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

		// Constructor with default values

		prior(const string &type="none", const string &str_info="")
			: type(type), str_info(str_info) {}
		void info() { cout << "prior : " << type << " ; " << str_info << endl; }
		virtual double llh(double x) { return 0; }
		double chi2(double x) { return -2*llh(x); }

	// These can be private again since we now only use 'prior' to access them.

	private:
		const string type;
		const string str_info;
};


class uniform
	: public prior
{
	public:
		uniform(double offset)
			: offset(offset), // constructor for things in 'uniform'...
			                  // ... and for things in 'prior'!
			prior("uniform", "offset = " + to_string(offset)) {} 
		virtual double llh(double x) { return offset; }

	private:
		const double offset;
};


int main(void)
{
	// Create a 'none' prior, and print info about it
	prior n;
	n.info();
	cout << "n.llh(1) = " << n.llh(1) << endl;
	cout << "n.chi2(1) = " << n.chi2(1) << endl;
	cout << "n.llh(2) = " << n.llh(2) << endl;
	cout << "n.chi2(2) = " << n.chi2(2) << endl << endl;

	// Create a 'uniform' prior, and print info about it
	uniform u(-0.2);
	u.info();
	cout << "u.llh(1) = " << u.llh(1) << endl;
	cout << "u.chi2(1) = " << u.chi2(1) << endl;
	cout << "u.llh(2) = " << u.llh(2) << endl;
	cout << "u.chi2(2) = " << u.chi2(2) << endl << endl;

	return 0;
};
