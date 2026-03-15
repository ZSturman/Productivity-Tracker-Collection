//
//  ActionStateListView.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import SwiftUI

struct ActionStateListView: View {
    @ObservedObject var vm: ActionStateListVM
    @ObservedObject var executionVM: ActionStateExecutionVM
    var dataService: DataService
    
    var body: some View {
        NavigationStack {
            VStack {
                List {
                    ForEach(vm.actionStates, id: \.id) { actionState in
                        Section {
                            
                            ZStack(alignment: .leading) {
                                NavigationLink(destination: ActionStateDetailView(vm: vm, actionState: actionState, executionVM: executionVM, dataService: dataService)) {
                                    EmptyView()
                                }
                                .opacity(0)
                                
                                ActionStateRowView(vm: vm, actionState: actionState, executionVM: executionVM, dataService: dataService) { selectedTrigger in
                                    executionVM.startExecution(triggerID: selectedTrigger.id!)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}





//struct ActionStateListView_Previews: PreviewProvider {
//    static var previews: some View {
//        ActionStateListView()
//    }
//}
