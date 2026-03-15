////
////  CreateEditActionStateViewNew.swift
////  Trackwell
////
////  Created by Zachary Sturman on 8/30/23.
////
//
//import SwiftUI
//
//struct CreateEditActionStateViewNew: View {
//    @ObservedObject var actionStateVM: ActionStateVM
//    @Environment(\.presentationMode) var presentationMode
//    @Binding var showCreateEditSheet: Bool
//    
//    @State var title: String = ""
//    @State var isAction: Bool = true
//    
//    @State private var showTriggerSheet = false
//    @State private var showInputSheet = false
//
//    var body: some View {
//        NavigationStack {
//            Form {
//                Text("\(actionStateVM.isNew ? "Is New" : "Is not New")")
//                GeneralInfo(actionStateVM: actionStateVM)
//            }
//            .navigationBarTitle(actionStateVM.isNew ? "Add ActionState" : "Edit ActionState")
//            .navigationBarItems(trailing: Button(action: actionStateVM.saveActionState) {
//                Text("Save")
//            })
//            .onAppear {
//                title = actionStateVM.actionState.title
//                isAction = actionStateVM.actionState.isAction
//            }
//
//        }
//    }
//}
//
//struct GeneralInfo: View {
//    @ObservedObject var actionStateVM: ActionStateVM
//    
//    var body: some View {
//        Section {
//            Picker("Choose Type", selection: $actionStateVM.actionState.isAction) {
//                Text("Action").tag(true)
//                Text("State").tag(false)
//            }
//            .pickerStyle(SegmentedPickerStyle())
//        }
//        
//        Section {
//            TextField("Title", text: $actionStateVM.actionState.title)
//        }
//    }
//}
