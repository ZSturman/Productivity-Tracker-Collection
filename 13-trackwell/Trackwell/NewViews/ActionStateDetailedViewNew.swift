////
////  ActionStateDetailedViewNew.swift
////  Trackwell
////
////  Created by Zachary Sturman on 8/30/23.
////
//
//import SwiftUI
//
//struct ActionStateDetailedViewNew: View {
//    @ObservedObject var vm: ActionStateListVM
//    @ObservedObject var actionStateVM: ActionStateVM
//    @Environment(\.presentationMode) var presentationMode
//    
//    @Binding var showCreateEditSheet: Bool
//    
//    var body: some View {
//        NavigationStack {
//            // Your existing content here...
//        }
//        .navigationTitle(actionStateVM.actionState.title)
//        .toolbar {
//            ToolbarItem(placement: .navigationBarTrailing) {
//                Button(action: {
//                    
//                    showCreateEditSheet = true
//                }, label: {
//                    Image(systemName: "pencil")
//                })
//            }
//
//            ToolbarItem(placement: .navigationBarTrailing) {
//                Button(action: {
//                    // ADD DELETE FUNCTIONALITY
//                    presentationMode.wrappedValue.dismiss()
//                },
//                label: {
//                    Image(systemName: "trash")
//                })
//            }
//
//        }
//        .sheet(isPresented: $showCreateEditSheet) {
//            CreateEditActionStateViewNew(actionStateVM: actionStateVM, showCreateEditSheet: $showCreateEditSheet)
//        }
//    }
//}
