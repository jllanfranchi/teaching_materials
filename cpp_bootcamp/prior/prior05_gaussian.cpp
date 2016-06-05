#include <iostream>
#include <sstream>
using namespace std;

class prior
{
	public:
		void info() { cout << "prior : " << type << " ; " << str_info << endl; }
		double chi2(double x) { return -2*llh(x); }
		virtual double llh(double) = 0; // <- pure virtual = 0

	protected:
		string type;
		string str_info;
};

class none
	: public prior
{
	public:
		none() {
			type = "none";
			str_info = "";
		}
		virtual double llh(double x) { return 0; }
};

class uniform
	: public prior
{
	public:
		uniform(double offset) : offset(offset) {
			type = "uniform";
			str_info = "offset = " + to_string(offset);
		}
		virtual double llh(double x) { return offset; }
		double get_offset() { return offset; }
		void set_offset(double y) { offset = y; }

	private:
		double offset;
};

class gaussian
	: public prior
{
	public:
		gaussian(double mean, double stddev) : mean(mean), stddev(stddev) {
			type = "Gaussian";
			str_info = "mean = " + to_string(mean) + ", stddev = " + to_string(stddev);
		}
		double llh(double x) { return -(x-mean)*(x-mean)/(2*stddev*stddev); }

		// Only defining getters, so outside world can't change our state
		// purists balk even at this (but purists drink deionized water, too)
		double get_mean() { return mean; }
		double get_stddev() { return stddev; }

	private:
		double mean;
		double stddev;
};

// Define a free function to work with priors.
//
// Must take pointer or reference to prior
//  -> cannot take value because pointer is abstract
//
//  -> but even if it weren't, a copy of one of the prior
//     classes will lose virtual functions (dynamic polymorphism)

double llh_freefunc(prior& p, double x) {
	return p.llh(x);
}


int main(void)
{
	none n;
	cout << "llh_freefunc(n, 1) = " << llh_freefunc(n, 1) << endl;

	uniform u(-0.2);
	cout << "llh_freefunc(u, 1) = " << llh_freefunc(u, 1) << endl;

	gaussian g(0, 1);
	cout << "llh_freefunc(g, 1) = " << llh_freefunc(g, 1) << endl << endl;

	return 0;
};
