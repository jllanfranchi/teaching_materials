#include <iostream>
#include <sstream>
using namespace std;

/*
 * "Virtual Function":
 *
 *		which version of an overriden function gets called is determined at
 *		runtime; example of "dynamic polymorphism."
 *
 * "Polymorphic Types":
 *
 * 		classes containing virtual function(s).
 */

class prior
{
	public:
		prior() : type("none"), str_info("") {}
		void info() { cout << "prior : " << type << " ; " << str_info << endl; }

		// which llh function is called by 'chi2' will be determined at runtime
		// via "vtables"

		virtual double llh(double x) { return 0; }
		double chi2(double x) { return -2*llh(x); }

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

		// not necessary to include 'virtual' here, but do anyway for clarity

		virtual double llh(double x) { return offset; }

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
	// chi2 now works for the derived class!
	cout << "u.chi2(1) = " << u.chi2(1) << endl << endl;

	cout << "u.llh(2) = " << u.llh(1) << endl;
	// and here as well
	cout << "u.chi2(2) = " << u.chi2(1) << endl << endl;

	return 0;
};
