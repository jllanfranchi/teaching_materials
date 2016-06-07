#include <iostream>
#include <sstream>
using namespace std;


class prior
{
	public:
		// constructor
		prior() : type("none"), str_info("") {}

		// pretty-print info
		void info() { cout << "prior : " << type << " ; " << str_info << endl; }

		// log-likelihood
		double llh(double x) { return 0; }

		// chi-square, in terms of llh
		double chi2(double x) { return -2*llh(x); }

	private:
		// keep these things protected from evil callers!
		const string type;
		const string str_info;
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

	return 0;
};
