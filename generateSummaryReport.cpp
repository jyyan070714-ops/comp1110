#include <iostream>
#include <string>
#include <iomanip>
#include <map>
#include <vector>
#include <algorithm>

using namespace std;

// --- 基础数据结构与内存管理 (由前位组员定义) ---
struct Data {
    string date;        // 格式: YYYY-MM-DD
    double amount;      
    string category;    
    string description; 
};

class BudgetAssistant {
private:
    Data* transactions; 
    int capacity;
    int count;

    // 动态数组扩容逻辑
    void grow() {
        capacity = (capacity == 0) ? 2 : capacity * 2;
        Data* newData = new Data[capacity];
        for (int i = 0; i < count; i++) {
            newData[i] = transactions[i];
        }
        delete[] transactions;
        transactions = newData;
    }

public:
    BudgetAssistant() : transactions(nullptr), capacity(0), count(0) {}
    
    ~BudgetAssistant() {
        delete[] transactions;
    }

    // 基础添加函数，确保统计功能有数据可读
    void addTransaction(string d, double a, string c, string desc) {
        if (count == capacity) grow();
        transactions[count].date = d;
        transactions[count].amount = a;
        transactions[count].category = c;
        transactions[count].description = desc;
        count++;
    }

    // ============================================================
    // --- 核心任务：Summary Statistics 实现 ---
    // ============================================================

    void generateSummaryReport() {
        if (count == 0) {
            cout << "\n[!] No records found. Summary cannot be generated." << endl;
            return;
        }

        double totalSpending = 0;
        map<string, double> categoryMap; // 用于按类别汇总
        map<string, double> monthlyMap;  // 用于按月统计趋势

        // 遍历动态数组执行计算
        for (int i = 0; i < count; i++) {
            totalSpending += transactions[i].amount;
            categoryMap[transactions[i].category] += transactions[i].amount;
            
            // 提取日期前7位 (YYYY-MM) 进行时间维度统计
            if (transactions[i].date.length() >= 7) {
                string month = transactions[i].date.substr(0, 7);
                monthlyMap[month] += transactions[i].amount;
            }
        }

        // --- 打印报表 ---
        cout << "\n========== FINANCIAL SUMMARY ==========" << endl;

        // 1. 总支出统计
        cout << "Total Transactions : " << count << endl;
        cout << "Total Expenditure  : HK$" << fixed << setprecision(2) << totalSpending << endl;

        // 2. 各类别支出明细
        cout << "\n[ Category Totals ]" << endl;
        for (auto const& [cat, val] : categoryMap) {
            double percentage = (val / totalSpending) * 100;
            cout << "- " << left << setw(12) << cat << ": HK$" 
                 << right << setw(8) << val 
                 << " (" << fixed << setprecision(1) << percentage << "%)" << endl;
        }

        // 3. Top-3 类别排名
        vector<pair<string, double>> sortedCats(categoryMap.begin(), categoryMap.end());
        sort(sortedCats.begin(), sortedCats.end(), [](const auto& a, const auto& b) {
            return a.second > b.second;
        });

        cout << "\n[ Top 3 Categories ]" << endl;
        int topLimit = (sortedCats.size() < 3) ? sortedCats.size() : 3;
        for (int i = 0; i < topLimit; i++) {
            cout << i + 1 << ". " << sortedCats[i].first << " (HK$" << sortedCats[i].second << ")" << endl;
        }

        // 4. 支出趋势 (按月汇总)
        cout << "\n[ Monthly Spending Trend ]" << endl;
        for (auto const& [month, val] : monthlyMap) {
            cout << "* " << month << ": HK$" << val << endl;
        }
        
        cout << "=======================================" << endl;
    }
};

// 实际提交时，main 函数通常由负责“菜单界面”的组员整合
int main() {
    // 只要你的组员在程序中调用了 generateSummaryReport()，它就能跑起来
    return 0;
}