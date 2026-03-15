////
////  ActionStateListViewNew.swift
////  Trackwell
////
////  Created by Zachary Sturman on 8/30/23.
////
//
//import SwiftUI
//
//struct ActionStateListViewNew: View {
//    @ObservedObject var vm: ActionStateListVM
//    @Binding var showCreateEditSheet: Bool
//    
//    var body: some View {
//        NavigationView {
//            List(vm.actionStates) { actionStateVM in
//                NavigationLink(destination: ActionStateDetailedViewNew(vm: vm, actionStateVM: actionStateVM, showCreateEditSheet: $showCreateEditSheet)) {
//                    Text(actionStateVM.actionState.title)
//                }
//            }
//            .navigationBarTitle("Action States")
//        }
//    }
//}
