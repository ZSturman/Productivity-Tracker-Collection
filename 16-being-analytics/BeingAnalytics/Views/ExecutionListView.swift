//
//  ExecutionListView.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//
 
import CoreData
import SwiftUI

struct ExecutionListView: View {
    var actionState: ActionState
    @ObservedObject var actionStateListVM: ActionStateListVM
    @ObservedObject var vm: ExecutionListVM

    init(actionStateListVM: ActionStateListVM, actionState: ActionState) {
        self.actionStateListVM = actionStateListVM
        self.actionState = actionState
        self.vm = ExecutionListVM(dataService: actionStateListVM.dataService, actionState: actionState)
    }
    
    var body: some View {
        List {
            ForEach(vm.groupedExecutions.keys.sorted(), id: \.self) { date in
                Section(header: Text(self.dateString(from: date))) {
                    ForEach(vm.groupedExecutions[date]!, id: \.id) { execution in
                        ExecutionRowView(execution: execution)
                    }
                }
            }
        }
    }

    func dateString(from date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .none
        return formatter.string(from: date)
    }
}


//struct ExecutionListView_Previews: PreviewProvider {
//    static var previews: some View {
//        ExecutionListView()
//    }
//}
