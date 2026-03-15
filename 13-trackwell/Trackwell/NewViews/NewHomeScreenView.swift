////
////  NewHomeScreenView.swift
////  Trackwell
////
////  Created by Zachary Sturman on 8/30/23.
////
//
//import SwiftUI
//
//struct NewHomeScreenView: View {
//    @ObservedObject var vm = ActionStateListVM()
//    @State private var showCreateEditSheet = false
//    
//    var body: some View {
//        NavigationStack {
//            VStack {
////                if $vm.actionStates.count == 0 {
////                    NoActionStateView()
////                } else {
////                    ActionStateListViewNew(vm: vm, showCreateEditSheet: $showCreateEditSheet)
////                }
//
//                    Text("\(vm.actionStates.count)")
//                    ActionStateListViewNew(vm: vm, showCreateEditSheet: $showCreateEditSheet)
//                
//            }
//            .toolbar {
//                ToolbarItem(placement: .navigationBarTrailing) {
//                    Button(action: {
//                        showCreateEditSheet.toggle()
//                    }, label: { Image(systemName: "plus")})
//
//                }
//            }
//                                    
//            .sheet(isPresented: $showCreateEditSheet) {
//                CreateEditActionStateViewNew(actionStateVM: ActionStateVM(actionStateListVM: vm), showCreateEditSheet: $showCreateEditSheet)
//            }
//        }
//    }
//}
//
//struct NewHomeScreenView_Previews: PreviewProvider {
//    static var previews: some View {
//        NewHomeScreenView()
//    }
//}
