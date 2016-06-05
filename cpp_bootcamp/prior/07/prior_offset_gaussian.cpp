#include <iostream>
#include <sstream>
using namespace std;

class prior
{
	public:
		prior(const string &type, const string &str_info)
			: type(type), str_info(str_info) {}
		void info() {
			cout << "prior : " << type << " ; " << str_info << endl;
		}
		double chi2(double x) { return -2*llh(x); }
		virtual double llh(double) = 0;

	protected:
		string type;
		string str_info;
};

class none
	: public prior
{
	public:
		none() : prior("none", "") {}
		virtual double llh(double x) { return 0; }
};

class uniform
	: public prior
{
	public:
		uniform(double offset) : offset(offset),
			prior("uniform", "offset = " + to_string(offset)) {}
		virtual double llh(double x) { return offset; }
		double get_offset() { return offset; }
		void set_offset(double y) { offset = y; }

	// change 'private' to 'protected' so our derived class can modify!
	protected:
		double offset;
};

class gaussian
	: public prior
{
	public:
		gaussian(double mean, double stddev) : mean(mean), stddev(stddev),
			prior("Gaussian", "mean = " + to_string(mean) + ", stddev = "
					+ to_string(stddev)) {}
		double llh(double x) { return -(x-mean)*(x-mean)/(2*stddev*stddev); }
		double get_mean() { return mean; }
		double get_stddev() { return stddev; }

	// change 'private' to 'protected' and remove 'const' declaration
	// so our derived class can modify!
	protected:
		double mean;
		double stddev;
};

// Offset Gaussian derives from 'gaussian' and 'uniform'
class offset_gaussian
	: public gaussian, public uniform
{
	public:
		offset_gaussian(double ofst, double mu, double sigma)
			: uniform(ofst), gaussian(mu, sigma) {}

			// can't do the following because not deriving from prior
			// (and to virtual base...

			//prior("offset Gaussian", "offset = " + to_string(ofst)
			//		+ ", mean = " + to_string(mu)
			//		+ ", stddev = " + to_string(sigma))
		double get_offset() { return offset; }
		double get_mean() { return mean; }
		double get_stddev() { return stddev; }
		void set_offset(double ofst) { offset = ofst; }
		void set_mean(double mu) { mean = mu; }
		void set_stddev(double sigma) { stddev = sigma; }
};


double llh_freefunc(prior& p, double x) {
	return p.llh(x);
}


int main(void)
{

	offset_gaussian og(-10, 0, 1);
	cout << "llh_freefunc(og, 1) = " << llh_freefunc(og, 1) << endl << endl;

	return 0;
};
