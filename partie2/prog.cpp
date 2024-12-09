#include "ProblemDecTiger.h"
#include "JESPExhaustivePlanner.h"

using namespace std;
int main() {
    ProblemDecTiger dectiger;
    JESPExhaustivePlanner jesp(3, &dectiger);
    jesp.Plan();
    cout << jesp.GetExpectedReward() << endl;
    cout << jesp.GetJointPolicy()->SoftPrint() << endl;
    return(0);
}