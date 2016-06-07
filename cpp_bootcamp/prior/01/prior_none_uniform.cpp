#include <iostream>
#include <sstream>
using namespace std;


//=============================================================================
//  What we had before...
//=============================================================================
class prior
{
	public:
		prior() : type("none"), str_info("") {}
		void info() { cout << "prior : " << type << " ; "
			<< str_info << endl; }
		double llh(double x) { return 0; }
		double chi2(double x) { return -2*llh(x); }

	private:
		string type;
		string str_info;
};


//=============================================================================
// What we're adding now...
//=============================================================================

class uniform
	: public prior // <== inherit publicly from 'prior' using this syntax
{
	public:
		// constructor for uniform; prior constructed by
		// default
		uniform(double offset) : offset(offset) {
			// populate data for this kind of prior
			type = "uniform";
			str_info = "offset = " + to_string(offset);
		}
		double llh(double x) { return offset; }

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
	cout << "u.chi2(1) = " << u.chi2(1) << endl << endl;
	cout << "u.llh(2) = " << u.llh(2) << endl;
	cout << "u.chi2(2) = " << u.chi2(2) << endl << endl;

	return 0;
};
