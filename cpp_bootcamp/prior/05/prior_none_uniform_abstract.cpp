#include <iostream>
#include <sstream>
using namespace std;

// Problem: Awkward to subclass "none" prior to get a non-none Prior.


/*
 * "Pure Virtual Function":
 *
 *		Function declared with ' = 0' appended; inheriting classes *must*
 *		implement, or they will not build.
 *
 * "Abstract Classes":
 *
 * 		Contain >= 1 /pure virtual/ functions (may implemented other functions)
 *
 * "Interface":
 *
 * 		Class that contains /only/ pure virtual functions (no implementations)
 */


// Solution to problem above:
//  -> Make an agnostic, abstract class "prior" not meant to be intialized
//  -> move "none" to its own class.

class prior
{
	public:
		// Constructor with no defaults ('prior' is agnostic now)
		prior(const string &type, const string &str_info) : type(type), str_info(str_info) {}

		// Might as well implement these, since they don't change
		// (of course you could still override these for an atypical case)

		void info() { cout << "prior : " << type << " ; " << str_info << endl; }
		double chi2(double x) { return -2*llh(x); }

		// Pure virtual functions must be implemented by inheritors
		// or they won't build!

		virtual double llh(double) = 0; // <- pure virtual = 0

	protected:
		const string type;
		const string str_info;
};

class none
	: public prior
{
	public:
		none() : prior("none", "") {
			//type = "none";
			//str_info = "";
		}
		virtual double llh(double x) { return 0; }
};

class uniform
	: public prior
{
	public:
		uniform(double offset) : offset(offset),
			prior("uniform", "offset = " + to_string(offset)) {}
		virtual double llh(double x) { return offset; }

		// Slight detour: getters and setters

		double get_offset() { return offset; }
		void set_offset(double y) { offset = y; }

	private:
		double offset;
};

int main(void)
{
	none n;
	n.info();
	cout << "n.llh(1) = " << n.llh(1) << endl;
	cout << "n.chi2(1) = " << n.chi2(1) << endl << endl;

	uniform u(-0.2);
	u.info();
	cout << "u.llh(1) = " << u.llh(1) << endl;
	cout << "u.chi2(1) = " << u.chi2(1) << endl << endl;

	// Try the setter and getter methods out
	cout << "SETTER / GETTER... " << endl;
	cout << "u.set_offset(-10.0);" << endl;
	u.set_offset(-10.0);
	cout << "u.get_offset() = " << u.get_offset() << endl;

	u.info();
	cout << "u.llh(1) = " << u.llh(1) << endl;
	cout << "u.chi2(1) = " << u.chi2(1) << endl << endl;

	/* 
	 *
	 * From some calling code, we won't care what /kind/ of prior we
	 * have, we just want to get the log likelihood.
	 *
	 *
	 */

	//    Assignment is disallowed to abstract base class
	//prior copy_of_u = u;
	
	// Abstract class can form reference to derived class
	prior& prior_reference_to_u = u;
	cout << "prior_reference_to_u.llh(1) = " << prior_reference_to_u.llh(1) << endl;
	cout << "prior_reference_to_u.chi2(1) = " << prior_reference_to_u.chi2(1) << endl << endl;

	//    ... but since 'prior' doesn't know about 'set_offset' function, you
	//    can't access this and other methods only defined in the child.
	//prior_reference_to_u.set_offset(-1);

	// Abstract class can be pointer to derived class
	prior* prior_pointer_to_u = &u;
	cout << "prior_pointer_to_u->llh(1) = " << prior_pointer_to_u->llh(1) << endl;
	cout << "prior_pointer_to_u->chi2(1) = " << prior_pointer_to_u->chi2(1) << endl << endl;

	//    ... again, 'prior' doesn't know about 'set_offset' function
	//prior_pointer_to_u->set_offset(-1);


	//    Cannot assign to sibling
	//none u_assigned_to_none = u;

	//    Cannot point to sibling
	//none* none_pointer_to_u = &u;

	//    Cannot reference sibling
	//none& none_pointer_to_u = u;


	return 0;
};
