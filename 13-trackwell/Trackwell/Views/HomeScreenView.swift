//
//  HomeScreenView.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/25/23.
//

import SwiftUI

struct HomeScreenView: View {
    @State private var showCreateEditView = false
    @ObservedObject var actionStateListVM = ActionStateListViewModel()

    var body: some View {
        NavigationStack {
            ActionStateListView(vm: actionStateListVM)
                .navigationBarItems(trailing: Button(action: {
                    showCreateEditView.toggle()
                }, label: {
                    Image(systemName: "plus")
                }))
                .sheet(isPresented: $showCreateEditView) {
                    CreateEditActionStateView(vm: CreateEditActionStateViewModel(actionStateListVM: self.actionStateListVM))
                }

        }
    }
}




struct HomeScreenView_Previews: PreviewProvider {
    static var previews: some View {
        HomeScreenView()
    }
}
